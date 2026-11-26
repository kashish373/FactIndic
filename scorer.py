import re, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

NAME = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
tok = AutoTokenizer.from_pretrained(NAME)
model = AutoModelForSequenceClassification.from_pretrained(NAME)
model.eval()
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(DEV)
labels = model.config.id2label

def split_sents(t):
    return [s.strip() for s in re.split(r"(?<=[.!?।])\s+", str(t)) if len(s.strip()) > 10]

def entail_score(article, sentence):
    words = str(article).split()
    chunks = [" ".join(words[i:i+150]) for i in range(0, max(len(words), 1), 120)]
    best = 0.0
    for ch in chunks:
        inp = tok(ch, sentence, truncation=True, max_length=512, return_tensors="pt").to(DEV)
        with torch.no_grad():
            probs = torch.softmax(model(**inp).logits, dim=-1)[0]
        for i, p in enumerate(probs):
            if labels[i].lower().startswith("entail"):
                best = max(best, float(p))
    return best

def score_summary(article, summary):
    """Returns a list of (sentence, score) pairs."""
    return [(s, round(entail_score(article, s), 2)) for s in split_sents(summary)]

if __name__ == "__main__":
    art = "भारत में प्रदूषण का स्तर लगातार बढ़ रहा है। दिल्ली में हवा की गुणवत्ता बहुत खराब हो गई है और सरकार ने स्कूल बंद करने का आदेश दिया है।"
    tests = []
    tests.append("भारत में प्रदूषण का स्तर बढ़ रहा है।")
    tests.append("प्रधानमंत्री ने 500 करोड़ रुपये के पैकेज की घोषणा की है।")
    tests.append("मुंबई में भारी बारिश के कारण बाढ़ आ गई है।")
    for t in tests:
        print(score_summary(art, t))