# FactIndic: Factuality-Aware Summarization for Indic and Code-Mixed Languages

CSET 346 - Natural Language Processing, Bennett University

**Team:** Kashish Kapoor (S24CSEU1764), Aaditri Chandok (S24CSEU1774), Ananya Bhatia (S24CSEU1979)
**Instructor:** Dr. Geetanjali Singh

## What this project does
Large language models write fluent summaries, but fluent does not mean true. FactIndic compares a **standard prompt** and a **factuality-aware prompt** on Hindi, Bengali and Hindi-English code-mixed text, and checks every summary sentence against the source article.

## Data and model
- Data: XL-Sum (Hindi and Bengali), first 20 articles of each; a synthetic code-mixed Hindi version built by word swapping
- Model: Gemma 3 4B, run locally with Ollama

## Metrics
NLI entailment score (chunked), number and entity grounding, ROUGE-1 and BERTScore (Precision, Recall, F1), summary length, compression ratio, inference time.

## Main findings (20 articles per dataset, so read as trends)
- A vague language rule made the factuality-aware prompt write English in 17 of 60 summaries; an explicit same-language rule removed this in our sample.
- A 512-token NLI checker underrates long Indic articles; checking the article in chunks raised support by 10 to 30 points.
- The factuality-aware prompt kept every number and English term grounded and scored higher on ROUGE and BERTScore, but NLI favored the standard prompt on Hindi.
- Code-mixing lowered NLI support for Hindi.

Final table: `results/FINAL_table.csv`

## How to run
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install torch transformers datasets evaluate rouge-score bert-score sentence-transformers pandas scikit-learn tqdm ollama streamlit
brew install ollama && brew services start ollama
ollama pull gemma3:4b

python load_data.py          # download data
python make_codemixed.py     # build code-mixed Hindi
python baseline.py           # standard prompt summaries
python factual.py            # factuality-aware summaries
python clean3.py             # remove preamble lines
python verify_chunked.py     # NLI factuality score
python entity_check.py       # number and entity check
python prf.py                # ROUGE and BERTScore
python final_table.py        # merge results
streamlit run app.py         # demo app
```

## Files
- `summarizer.py`, `scorer.py`, `app.py`: demo app
- `results/`: summaries and metric files
- `data/` is not uploaded; run `load_data.py` to recreate it

## Limitations
Only 20 articles per dataset and one 4B model; code-mixed text is synthetic; the NLI score is an estimate; timing is approximate.