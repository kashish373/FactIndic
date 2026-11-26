import ollama, time

MODEL = "gemma3:4b"

STANDARD = ("Summarize the following article in 2-3 sentences. "
            "Write the summary in the same language as the article.\n\n"
            "Article:\n{text}")

FACTUAL = """You are a careful summarizer. Summarize the article below in 2-3 sentences.
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

def summarize(text, mode="factual"):
    prompt = (FACTUAL if mode == "factual" else STANDARD).format(text=text)
    start = time.time()
    r = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return r["message"]["content"].strip(), round(time.time() - start, 1)

if __name__ == "__main__":
    sample = "भारत में प्रदूषण का स्तर लगातार बढ़ रहा है। दिल्ली में हवा की गुणवत्ता बहुत खराब हो गई है और सरकार ने स्कूल बंद करने का आदेश दिया है।"
    for mode in ["standard", "factual"]:
        s, t = summarize(sample, mode)
        print(mode.upper(), f"({t} sec):", s)
        print()