"""
Courbe de progression — Online Learning
========================================
Lit les resultats sauvegardes par online_evaluation_iso.py
et trace la courbe Top-1 / Top-3 en fonction des phrases vues.
"""

import json
import os
import sys

RESULTS_PATH = "data/online_learning_results.json"

def plot_ascii(checkpoints):
    """Affichage ASCII si matplotlib n'est pas disponible."""
    print("\nProgression Top-1 (ASCII) :")
    print(f"{'Phrases':>10} | {'Top-1':>6} | Bar")
    print("-" * 50)
    for cp in checkpoints:
        bar = "█" * int(cp["top1"] / 2)
        print(f"{cp['phrases_vues']:>10} | {cp['top1']:>5}% | {bar}")

def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"Fichier introuvable : {RESULTS_PATH}")
        print("Lance d'abord : python src/evaluation/online_evaluation_iso.py")
        sys.exit(1)

    with open(RESULTS_PATH) as f:
        checkpoints = json.load(f)

    phrases = [cp["phrases_vues"] for cp in checkpoints]
    top1    = [cp["top1"]         for cp in checkpoints]
    top3    = [cp["top3"]         for cp in checkpoints]

    # Affichage ASCII toujours disponible
    plot_ascii(checkpoints)

    # Graphique matplotlib si disponible
    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 5))
        plt.plot(phrases, top1, 'b-o', label='Top-1', linewidth=2)
        plt.plot(phrases, top3, 'g-s', label='Top-3', linewidth=2)
        plt.xlabel("Phrases vues (online learning)")
        plt.ylabel("Accuracy (%)")
        plt.title("Online Learning — Progression du modele n-gram\n(ISO 7240-14, corpus nettoye)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig("data/online_learning_curve.png", dpi=150)
        plt.show()
        print("\nGraphique sauve -> data/online_learning_curve.png")

    except ImportError:
        print("\n(matplotlib non disponible — installe avec: pip install matplotlib)")

if __name__ == "__main__":
    main()