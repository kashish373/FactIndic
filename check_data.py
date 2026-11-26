import pandas as pd

for lang in ["hindi", "bengali"]:
    df = pd.read_csv(f"data/{lang}_200.csv")
    print("-----", lang, "-----")
    print("Rows:", len(df))
    print("Average article words:", int(df["words"].mean()))
    print("First article (first 300 chars):")
    print(df["text"][0][:300])
    print("Reference summary:")
    print(df["summary"][0])