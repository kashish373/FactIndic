import pandas as pd

for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both_{name}.csv")
    print("=====", name, "=====")
    print("Avg baseline time:", round(df["baseline_time"].mean(), 1), "sec")
    print("Avg factual time:", round(df["factual_time"].mean(), 1), "sec")
    print("BASELINE:", df["baseline_summary"][0])
    print("FACTUAL:", df["factual_summary"][0])
    print("REFERENCE:", df["summary"][0])
    print()