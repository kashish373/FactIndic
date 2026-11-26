import ollama, time
import pandas as pd

MODEL = "gemma3:4b"
N = 20

PROMPT = """You are a careful summarizer. Summarize the article below in 2-3 sentences.
IMPORTANT: Write the summary in the SAME LANGUAGE and SCRIPT as the article. Never write in English unless the article itself is in English.
Rules:
1. Use ONLY information that is stated in the article. Do not add anything from your own knowledge.
2. Keep all names, places, numbers and dates exactly as in the article.
3. If the article already contains English words, keep them as they are. Do not translate the summary into English.
4. Do not guess or interpret. If something is unclear, leave it out.
5. Output only the summary, with no introduction or notes.

Article:
{text}

Summary:"""

jobs = [
    ("hindi",    "results/baseline_hindi.csv",    "text"),
    ("hindi_cm", "results/baseline_hindi_cm.csv", "text_cm"),
    ("bengali",  "results/baseline_bengali.csv",  "text"),
]

for name, path, col in jobs:
    df = pd.read_csv(path)
    outputs, times = [], []
    for i, text in enumerate(df[col]):
        start = time.time()
        r = ollama.chat(model=MODEL,
                        messages=[{"role": "user", "content": PROMPT.format(text=text)}])
        times.append(round(time.time() - start, 2))
        outputs.append(r["message"]["content"].strip())
        print("FACTUAL2", name, i + 1, "/", N, "done", times[-1], "sec", flush=True)
    df["factual_summary"] = outputs
    df["factual_time"] = times
    df.to_csv(f"results/both2_{name}.csv", index=False)

print("All done")