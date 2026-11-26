import pandas as pd, re

def clean(t):
    t = str(t).strip()
    parts = t.split("\n\n", 1)
    first = parts[0]
    if len(parts) == 2 and (":" in first[-3:] or "सारांश" in first or "সংক্ষেপ" in first or "সারাংশ" in first):
        t = parts[1]
    return t.strip()

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both_{name}.csv")
    for m in ["baseline", "factual"]:
        df[f"{m}_summary"] = df[f"{m}_summary"].apply(clean)
    df.to_csv(f"results/both_{name}.csv", index=False)
print("cleaned")