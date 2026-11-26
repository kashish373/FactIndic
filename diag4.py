import re
import pandas as pd

def tokens(t):
    nums = re.findall(r"[0-9\u0966-\u096F\u09E6-\u09EF]+", str(t))
    latin = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", str(t))]
    return set(nums) | set(latin)

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both3_{name}.csv")
    src = "text_cm" if name == "hindi_cm" else "text"
    bad = []
    for art, summ in zip(df[src], df["baseline_summary"]):
        bad += sorted(tokens(summ) - tokens(art))
    print(name, bad)