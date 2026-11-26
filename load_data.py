from datasets import load_dataset
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

for lang in ["hindi", "bengali"]:
    ds = load_dataset("csebuetnlp/xlsum", lang, split="test")
    df = ds.to_pandas()[["text", "summary"]]
    df["words"] = df["text"].str.split().str.len()
    df = df[(df["words"] >= 150) & (df["words"] <= 800)]
    df = df.dropna().head(200)
    df.to_csv(f"data/{lang}_200.csv", index=False)
    print(lang, "saved:", len(df), "rows")