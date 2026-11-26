import re
import pandas as pd

def tokens(t):
    t = re.sub(r"[2-3\u09E8-\u09E9\u0968-\u0969]\s*[-\u2013]\s*[2-3\u09E8-\u09E9\u0968-\u0969]", " ", str(t))
    nums = re.findall(r"[0-9\u0966-\u096F\u09E6-\u09EF]+", t)
    latin = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", t)]
    return set(nums), set(latin)

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both4_{name}.csv")
    src_col = "text_cm" if name == "hindi_cm" else "text"
    for method in ["baseline", "factual"]:
        tp = fp = 0
        for art, summ in zip(df[src_col], df[f"{method}_summary"]):
            a_n, a_l = tokens(art)
            s_n, s_l = tokens(summ)
            s_all, a_all = s_n | s_l, a_n | a_l
            tp += len(s_all & a_all)
            fp += len(s_all - a_all)
        prec = tp / (tp + fp) if (tp + fp) else 0
        rows.append({"dataset": name, "method": method,
                     "supported_items": tp, "unsupported_items": fp,
                     "fact_precision": round(prec, 3)})
        print(rows[-1])

pd.DataFrame(rows).to_csv("results/metrics_entity3.csv", index=False)
print("All done")