import re
import pandas as pd

def is_english(t):
    latin = len(re.findall(r"[A-Za-z]", str(t)))
    indic = len(re.findall(r"[\u0900-\u097F\u0980-\u09FF]", str(t)))
    return latin > indic

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both2_{name}.csv")
    for m in ["baseline", "factual"]:
        n = int(df[f"{m}_summary"].apply(is_english).sum())
        rows.append({"dataset": name, "method": m, "english_summaries": n, "out_of": len(df)})
        print(rows[-1])
pd.DataFrame(rows).to_csv("results/metrics_language2.csv", index=False)