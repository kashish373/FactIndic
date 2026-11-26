import pandas as pd

swap = {
    "सरकार": "government", "पुलिस": "police", "अदालत": "court",
    "चुनाव": "election", "प्रधानमंत्री": "Prime Minister",
    "मंत्री": "minister", "अस्पताल": "hospital", "स्कूल": "school",
    "पाकिस्तान": "Pakistan", "भारत": "India", "रिपोर्ट": "report",
    "प्रदूषण": "pollution", "स्तर": "level", "बढ़": "increase",
    "खेल": "sports", "मैच": "match", "टीम": "team",
    "कंपनी": "company", "बाज़ार": "market", "अर्थव्यवस्था": "economy",
    "विश्वविद्यालय": "university", "छात्र": "student", "परीक्षा": "exam",
    "गिरफ़्तार": "arrest", "मामला": "case", "जाँच": "investigation",
    "सुरक्षा": "security", "आदेश": "order", "वकील": "lawyer",
}

df = pd.read_csv("data/hindi_200.csv")
df["text_cm"] = df["text"]
for hi_word, en_word in swap.items():
    df["text_cm"] = df["text_cm"].str.replace(hi_word, en_word, regex=False)

df.to_csv("data/hindi_codemixed_200.csv", index=False)
print(df["text"][0][:200])
print("--- code-mixed ---")
print(df["text_cm"][0][:200])