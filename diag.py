import re
import pandas as pd

for name in ["hindi", "bengali"]:
    df = pd.read_csv(f"results/both_{name}.csv")
    counts = df["factual_summary"].apply(lambda t: len(re.findall(r"[A-Za-z]{3,}", str(t))))
    print("=====", name, "=====")
    print("English words per factual summary:", list(counts))
    worst = counts.idxmax()
    print("Worst row:", worst)
    print(str(df["factual_summary"][worst])[:600])
    print()