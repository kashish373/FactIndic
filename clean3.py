import pandas as pd, re

def clean(t):
    t = str(t).strip()
    parts = re.split(r"\n\s*\n", t, maxsplit=1)
    first = parts[0].strip()
    if len(parts) == 2 and first.endswith((":", "\uff1a")) and len(first.split()) < 30:
        return parts[1].strip()
    return t

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both3_{name}.csv")
    before = df["baseline_summary"].copy()
    df["baseline_summary"] = df["baseline_summary"].apply(clean)
    changed = int((before != df["baseline_summary"]).sum())
    print(name, "baseline summaries changed:", changed, "of", len(df))
    df.to_csv(f"results/both4_{name}.csv", index=False)
print("cleaned")