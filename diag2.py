import re
import pandas as pd

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both2_{name}.csv")
    counts = df["baseline_summary"].apply(lambda t: len(re.findall(r"[A-Za-z]{3,}", str(t))))
    print(name, "English words per baseline summary:", list(counts))