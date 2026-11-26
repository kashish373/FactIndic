import re
import pandas as pd

df = pd.read_csv("results/both2_hindi.csv")
for i in [2, 5, 7, 12]:
    t = str(df["baseline_summary"][i])
    print("ROW", i, "->", re.findall(r"[A-Za-z]{3,}", t))
    print(t[:200])
    print()