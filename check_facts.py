import pandas as pd

hi = pd.read_csv("data/hindi_200.csv")["text"][0]
bn = pd.read_csv("data/bengali_200.csv")["text"][0]

print("Hindi: '29' or '२९' in article:", "29" in hi or "२९" in hi)
print("Hindi: 'सितंबर' or 'सितम्बर' in article:", "सितंबर" in hi or "सितम्बर" in hi)
print("Bengali: 'জিনপিং' in article:", "জিনপিং" in bn)
print("Bengali: 'হিউম্যান রাইটস ওয়াচ' in article:", "হিউম্যান রাইটস ওয়াচ" in bn)
print("Bengali: 'অ্যামনেস্টি' in article:", "অ্যামনেস্টি" in bn)
print("Bengali: 'জিনজিয়াং' in article:", "জিনজিয়াং" in bn)