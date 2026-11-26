import pandas as pd

rows = []
for name in ["hindi", "hindi_cm", "bengali"]:
    df = pd.read_csv(f"results/both4_{name}.csv")
    src_col = "text_cm" if name == "hindi_cm" else "text"
    src_len = df[src_col].str.split().str.len()
    for m in ["baseline", "factual"]:
        s_len = df[f"{m}_summary"].str.split().str.len()
        rows.append({
            "dataset": name, "method": m,
            "avg_summary_words": round(s_len.mean(), 1),
            "compression_ratio": round((s_len / src_len).mean(), 3),
            "avg_time_sec": round(df[f"{m}_time"].mean(), 1),
        })
out = pd.DataFrame(rows)
out.to_csv("results/metrics_basic_final.csv", index=False)
print(out.to_string(index=False))