import pandas as pd
from rouge_score import rouge_scorer, tokenizers
from bert_score import score as bert_score

class WS(tokenizers.Tokenizer):
    def tokenize(self, text):
        return str(text).lower().split()

sc = rouge_scorer.RougeScorer(["rouge1", "rougeL"], tokenizer=WS())

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both4_{name}.csv")
    lang = "bn" if name == "bengali" else "hi"
    refs = df["summary"].astype(str).tolist()
    for m in ["baseline", "factual"]:
        cands = df[f"{m}_summary"].astype(str).tolist()
        r1 = [sc.score(r, c)["rouge1"] for r, c in zip(refs, cands)]
        rl = [sc.score(r, c)["rougeL"] for r, c in zip(refs, cands)]
        P, R, F = bert_score(cands, refs, lang=lang, device="cpu")
        row = {
            "dataset": name, "method": m,
            "rouge1_P": round(sum(x.precision for x in r1) / len(r1), 3),
            "rouge1_R": round(sum(x.recall for x in r1) / len(r1), 3),
            "rouge1_F1": round(sum(x.fmeasure for x in r1) / len(r1), 3),
            "rougeL_F1": round(sum(x.fmeasure for x in rl) / len(rl), 3),
            "bert_P": round(P.mean().item(), 3),
            "bert_R": round(R.mean().item(), 3),
            "bert_F1": round(F.mean().item(), 3),
        }
        rows.append(row)
        print(row, flush=True)

pd.DataFrame(rows).to_csv("results/metrics_prf.csv", index=False)
print("All done")