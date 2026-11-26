import ollama, time, os
import pandas as pd

MODEL = "gemma3:4b"
N = 20  # start small, we scale up later

PROMPT = ("Summarize the following article in 2-3 sentences. "
          "Write the summary in the same language as the article.\n\n"
          "Article:\n{text}")

jobs = [
    ("hindi",      "data/hindi_200.csv",            "text"),
    ("hindi_cm",   "data/hindi_codemixed_200.csv",  "text_cm"),
    ("bengali",    "data/bengali_200.csv",          "text"),
]

os.makedirs("results", exist_ok=True)

for name, path, col in jobs:
    df = pd.read_csv(path).head(N)
    outputs, times = [], []
    for i, text in enumerate(df[col]):
        start = time.time()
        r = ollama.chat(model=MODEL,
                        messages=[{"role": "user", "content": PROMPT.format(text=text)}])
        times.append(round(time.time() - start, 2))
        outputs.append(r["message"]["content"].strip())
        print(name, i + 1, "/", N, "done", times[-1], "sec")
    df["baseline_summary"] = outputs
    df["baseline_time"] = times
    df.to_csv(f"results/baseline_{name}.csv", index=False)

print("All done")