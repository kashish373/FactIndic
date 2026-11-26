import pandas as pd, re

def clean(t):
    t = str(t).strip()
    # drop any leading English line(s) up to the first Indic character
    m = re.search(r"[\u0900-\u097F\u0980-\u09FF]", t)
    if m:
        t = t[m.start():]
    # cut off any trailing English translation block
    parts = re.split(r"\n\s*\n", t)
    keep = []
    for p in parts:
        latin = len(re.findall(r"[A-Za-z]", p))
        indic = len(re.findall(r"[\u0900-\u097F\u0980-\u09FF]", p))
        if indic >= latin:
            keep.append(p)
    return "\n\n".join(keep).strip()

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both2_{name}.csv")
    df["baseline_summary"] = df["baseline_summary"].apply(clean)
    df.to_csv(f"results/both3_{name}.csv", index=False)
print("cleaned")