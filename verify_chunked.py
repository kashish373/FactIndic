import re, torch
import pandas as pd
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
    chunks = [" ".join(words[i:i+150]) for i in range(0, len(words), 120)]
    best = 0.0
    for ch in chunks:
        inp = tok(ch, sentence, truncation=True, max_length=512, return_tensors="pt").to(DEV)
        with torch.no_grad():
            probs = torch.softmax(model(**inp).logits, dim=-1)[0]
        for i, p in enumerate(probs):
            if labels[i].lower().startswith("entail"):
                best = max(best, float(p))
    return best

def summary_score(article, summary):
    sents = split_sents(summary)
    if not sents:
        return 0.0, 0.0
    scores = [entail_score(article, s) for s in sents]
    supported = sum(1 for s in scores if s >= 0.5) / len(scores)
    return sum(scores) / len(scores), supported

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both4_{name}.csv")
    src_col = "text_cm" if name == "hindi_cm" else "text"
    for method in ["baseline", "factual"]:
        avg_e, sup = [], []
        for art, summ in zip(df[src_col], df[f"{method}_summary"]):
            a, s = summary_score(art, summ)
            avg_e.append(a); sup.append(s)
            print(name, method, len(avg_e), "/ 20", flush=True)
        rows.append({"dataset": name, "method": method,
                     "avg_entailment": round(sum(avg_e)/len(avg_e), 3),
                     "pct_sentences_supported": round(100*sum(sup)/len(sup), 1)})
        print(rows[-1])

pd.DataFrame(rows).to_csv("results/metrics_factuality_v4.csv", index=False)
print("All done")