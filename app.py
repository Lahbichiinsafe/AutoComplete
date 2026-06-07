"""
Serveur Flask — Interface web d'autocompletion intelligente
===========================================================

"""

from flask import Flask, request, jsonify, send_from_directory
import sys, os, re
from pathlib import Path

# Ajoute le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from autocomplete.ngram_autocomplete         import NgramAutocomplete
from autocomplete.lm_finetuned_autocomplete  import LMFinetunedAutocomplete
from autocomplete.hybrid_autocomplete        import HybridAutocomplete

app = Flask(__name__, static_folder="static")

# --- Chemins ---
CORPUS_PATH   = "data/scenarios/scenarios_fire_detection_clean.txt"
GLOSSARY_PATH = "data/glossaires/glossaire_fire_detection_and_alarm_systems.txt"
GPT2_DIR      = "models/gpt2_fire_detection"
QWEN2_DIR     = "models/qwen2_fire_detection"

# --- Chargement des modeles au demarrage ---
print("Chargement du N-gram...")
ngram = NgramAutocomplete(
    n=3,
    glossary_path=GLOSSARY_PATH if os.path.exists(GLOSSARY_PATH) else None,
    corpus_path=CORPUS_PATH
)

lm, lm_name = None, "N-gram only"
for model_dir, base, name in [
    (GPT2_DIR,  "gpt2",            "GPT-2"),
    (QWEN2_DIR, "Qwen/Qwen2-0.5B", "Qwen2-0.5B"),
]:
    if os.path.exists(model_dir):
        print(f"Chargement LM : {name}...")
        lm = LMFinetunedAutocomplete(model_name=base, output_dir=model_dir)
        lm_name = name
        break

if lm:
    hybrid = HybridAutocomplete(ngram=ngram, lm=lm, confidence_threshold=10.0)
    print(f"Hybride pret : N-gram + {lm_name}")
else:
    hybrid = None
    print("Mode N-gram uniquement (pas de LM trouve)")

def tokenize(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/suggest", methods=["POST"])
def suggest():
    data    = request.get_json()
    text    = data.get("text", "").strip()
    prefix  = data.get("prefix", "")   # lettres deja tapees du mot en cours
    top_k   = data.get("top_k", 5)

    words   = tokenize(text)
    context = words if not prefix else words  # contexte = tous les mots complets

    model   = hybrid if hybrid else ngram
    source  = "ngram"

    try:
        if hybrid:
            source  = hybrid.which_model(context, prefix)
        results = model.predict(context, prefix, top_k=top_k)
        suggestions = [{"word": r[0], "score": r[1], "glossary": r[2]}
                       for r in results]
    except Exception as e:
        suggestions = []
        source = "error"

    return jsonify({
        "suggestions": suggestions,
        "source": source,
        "lm_name": lm_name,
        "context_words": len(words)
    })

@app.route("/info")
def info():
    return jsonify({
        "lm": lm_name,
        "ngram": "N-gram n=3",
        "mode": "hybrid" if hybrid else "ngram",
        "corpus": CORPUS_PATH
    })

if __name__ == "__main__":
    print("\n=== AutoComplete Server ===")
    print(f"Modele : {'Hybride N-gram + ' + lm_name if hybrid else 'N-gram seul'}")
    print("Ouvre http://localhost:5000 dans ton navigateur\n")
    app.run(debug=False, port=5000)