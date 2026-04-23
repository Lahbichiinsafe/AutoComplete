from pathlib import Path
import re


def extract_text_from_pdf(pdf_path: str) -> list:
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pip install pdfplumber")

    sentences = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line = line.strip()
                if len(re.findall(r'\b[a-zA-Z]{2,}\b', line)) >= 4:
                    sentences.append(line)

    sentences = list(dict.fromkeys(sentences))  # dédoublonnage ordre conservé
    print(f"{len(sentences)} lines extracted from PDF")
    return sentences


def extract_glossary_from_pdf(pdf_path: str, top_n: int = 500) -> list:
    from collections import Counter
    stop_words = {
        'the','a','an','and','or','but','in','on','at','to','for','of','with',
        'by','from','as','is','was','are','were','be','been','have','has','had',
        'do','does','did','will','would','should','could','may','might','can',
        'if','than','this','that','these','those','their','there','they','them',
        'what','which','who','when','where','all','each','every','some','such',
        'no','not','only','it','its','after','before','into','through','shall'
    }
    lines = extract_text_from_pdf(pdf_path)
    words = re.findall(r'\b[a-z]{3,}\b', " ".join(lines).lower())
    counter = Counter(w for w in words if w not in stop_words)
    terms = [w for w, _ in counter.most_common(top_n)]
    print(f"{len(terms)} glossary terms extracted")
    return terms


def save_corpus(lines: list, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Corpus saved: {output_path}")


def save_glossary(terms: list, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(terms))
    print(f"Glossary saved: {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python extract_from_pdf.py <path/to/file.pdf>")
        sys.exit(1)
    pdf_path = sys.argv[1]
    domain = Path(pdf_path).stem.split()[0].lower()
    lines = extract_text_from_pdf(pdf_path)
    save_corpus(lines, f"data/scenarios/scenarios_{domain}.txt")
    terms = extract_glossary_from_pdf(pdf_path)
    save_glossary(terms, f"data/glossaires/glossaire_{domain}.txt")
