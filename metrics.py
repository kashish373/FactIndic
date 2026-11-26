import pandas as pd

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both_{name}.csv")
    src_col = "text_cm" if name == "hindi_cm" else "text"
    src_len = df[src_col].str.split().str.len()
    for method in ["baseline", "factual"]:
        s_len = df[f"{method}_summary"].str.split().str.len()
        rows.append({
            "dataset": name,
            "method": method,
            "avg_summary_words": round(s_len.mean(), 1),
            "compression_ratio": round((s_len / src_len).mean(), 3),
            "avg_time_sec": round(df[f"{method}_time"].mean(), 1),
        })

out = pd.DataFrame(rows)
print(out.to_string(index=False))
out.to_csv("results/metrics_basic.csv", index=False)