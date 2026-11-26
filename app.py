import html, re
import pandas as pd
import streamlit as st
from summarizer import summarize
from scorer import score_summary

st.set_page_config(page_title="FactIndic", page_icon="🔍", layout="wide")

CSS = """
<style>
.hero {padding: 34px 36px; border-radius: 22px; margin-bottom: 20px; color: white;
  background: linear-gradient(120deg, #4338ca 0%, #7c3aed 45%, #db2777 100%);
  box-shadow: 0 10px 30px rgba(124,58,237,0.35);}
.hero h1 {margin: 0; font-size: 2.6rem; color: white; letter-spacing: -0.5px;}
.hero p {margin: 8px 0 14px 0; font-size: 1.1rem; color: rgba(255,255,255,0.92);}
.pill {display: inline-block; padding: 4px 12px; margin: 0 6px 6px 0; border-radius: 999px;
  background: rgba(255,255,255,0.18); font-size: 0.85rem; color: white;}
.card {border-radius: 18px; padding: 20px 22px; margin-bottom: 12px; color: #f3f4f6;
  background: #1b1b27; border: 1px solid #2e2e42; line-height: 1.7;}
.card h3 {margin: 0 0 10px 0; color: #ffffff; font-size: 1.25rem;}
.chip {display: inline-block; padding: 4px 12px; border-radius: 999px; margin: 4px 6px 4px 0;
  font-size: 0.82rem; background: #2a2a3d; color: #d1d5db;}
.scorebox {display: flex; align-items: center; gap: 18px; padding: 14px 18px; margin: 10px 0;
  border-radius: 16px; background: #1b1b27; border: 1px solid #2e2e42; color: #e5e7eb;}
.gauge {width: 88px; height: 88px; border-radius: 50%; display: grid; place-items: center;
  background: conic-gradient(var(--c) calc(var(--p) * 1%), #33334a 0);}
.gin {width: 68px; height: 68px; border-radius: 50%; background: #1b1b27; display: grid;
  place-items: center; font-weight: 800; font-size: 1.15rem; color: #ffffff;}
.sent {padding: 10px 14px; margin: 7px 0; border-radius: 10px; border-left: 6px solid;
  background: #1f1f2e; color: #e5e7eb; line-height: 1.6;}
.s-good {border-color: #22c55e;} .s-mid {border-color: #f59e0b;} .s-bad {border-color: #ef4444;}
.sc {font-weight: 800; margin-right: 8px;}
.winner {padding: 14px 20px; border-radius: 14px; margin: 14px 0; font-size: 1.05rem; font-weight: 600;
  background: linear-gradient(90deg, #14532d, #166534); color: #dcfce7; border: 1px solid #22c55e;}
.tie {background: linear-gradient(90deg, #1e3a8a, #1d4ed8); color: #dbeafe; border-color: #60a5fa;}
.note {opacity: 0.75; font-size: 0.85rem;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

SAMPLES = {
    "Hindi": ("दिल्ली में पिछले एक हफ्ते से वायु प्रदूषण का स्तर लगातार बढ़ रहा है। मंगलवार को कई इलाकों में "
              "हवा की गुणवत्ता का सूचकांक 400 से ऊपर पहुंच गया। सरकार ने प्राथमिक स्कूलों को दो दिन के लिए "
              "बंद करने का आदेश दिया है। विशेषज्ञों का कहना है कि अगले हफ्ते तक स्थिति में सुधार की संभावना "
              "कम है। अस्पतालों में सांस की बीमारी के मरीज़ों की संख्या भी बढ़ गई है।"),
    "Code-mixed": ("Delhi में पिछले एक हफ्ते से pollution का level लगातार बढ़ रहा है। मंगलवार को कई areas में "
                   "air quality index 400 से ऊपर पहुंच गया। government ने primary schools को दो दिन के लिए "
                   "बंद करने का order दिया है। experts का कहना है कि अगले हफ्ते तक situation में सुधार की "
                   "संभावना कम है। hospital में सांस की बीमारी के patients की संख्या भी बढ़ गई है।"),
    "Bengali": ("কলকাতায় গত তিন দিন ধরে প্রবল বৃষ্টি হচ্ছে। বুধবার সকালে শহরের অনেক এলাকায় জল জমে যায়। "
                "রাজ্য সরকার জানিয়েছে, পরিস্থিতি সামলাতে ২০০ জন কর্মী নিয়োগ করা হয়েছে। আবহাওয়া দপ্তর "
                "জানিয়েছে, আগামী দুই দিন বৃষ্টি চলতে পারে। অনেক স্কুল বৃহস্পতিবার বন্ধ রাখা হয়েছে।"),
}

def load_sample(name):
    st.session_state["article"] = SAMPLES[name]

def detect(text):
    deva = len(re.findall(r"[\u0900-\u097F]", text))
    beng = len(re.findall(r"[\u0980-\u09FF]", text))
    lat = len(re.findall(r"[A-Za-z]", text))
    total = max(deva + beng + lat, 1)
    if deva + beng == 0:
        return "English"
    name = "Bengali" if beng > deva else "Hindi"
    return name + " + English (code-mixed)" if lat / total > 0.10 else name

LABEL = re.compile(r"^\s*\**\s*(english|hindi|bengali|bangla)?\s*(summary|translation)\s*:?\s*\**\s*$", re.I)

def strip_preamble(t):
    lines = str(t).strip().split("\n")
    out = [ln for ln in lines if not LABEL.match(ln)]
    if out and out[0].strip().endswith(":") and len(out[0].split()) < 30:
        out = out[1:]
    return "\n".join(out).replace("**", "").strip()

def band(x):
    return "good" if x >= 0.7 else "mid" if x >= 0.5 else "bad"

COLORS = {"good": "#22c55e", "mid": "#f59e0b", "bad": "#ef4444"}

def gauge(avg, supported, total):
    b = band(avg)
    return (f'<div class="scorebox"><div class="gauge" style="--p:{avg * 100:.0f};--c:{COLORS[b]}">'
            f'<div class="gin">{avg:.2f}</div></div><div><b>Factuality score</b><br>'
            f'<span class="note">{supported} of {total} sentences supported by the article</span></div></div>')

with st.sidebar:
    st.header("⚙️ Settings")
    clean_on = st.toggle("Remove preamble and labels", value=True)
    skip_short = st.toggle("Ignore very short fragments", value=True)
    st.markdown("---")
    st.markdown("**Score guide**")
    st.markdown("🟢 0.70+ supported")
    st.markdown("🟠 0.50 to 0.69 weak")
    st.markdown("🔴 below 0.50 unsupported")
    st.markdown("---")
    st.caption("Gemma 3 4B runs locally. Checker: multilingual NLI over article chunks. "
               "Scores are estimates, not proof.")

st.markdown(
    '<div class="hero"><h1>🔍 FactIndic</h1>'
    '<p>Factuality-aware summarization for Hindi, Bengali and code-mixed text.</p>'
    '<span class="pill">🇮🇳 Hindi</span><span class="pill">বাংলা Bengali</span>'
    '<span class="pill">🔀 Code-mixed</span><span class="pill">🛡️ Fact-checked per sentence</span>'
    '<span class="pill">💻 Runs locally</span></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✨ Try it", "📊 Project results"])

with tab1:
    st.markdown("**Quick samples**")
    b1, b2, b3, _ = st.columns([1, 1, 1, 4])
    b1.button("Hindi", on_click=load_sample, args=("Hindi",), use_container_width=True)
    b2.button("Code-mixed", on_click=load_sample, args=("Code-mixed",), use_container_width=True)
    b3.button("Bengali", on_click=load_sample, args=("Bengali",), use_container_width=True)

    st.text_area("Paste your article", height=200, key="article",
                 placeholder="Paste a Hindi, Bengali or code-mixed article here...")
    go = st.button("✨ Summarize and fact-check", type="primary")
    article = st.session_state.get("article", "")

    if go:
        if len(article.split()) < 20:
            st.warning("Please paste a longer article (at least 20 words).")
        else:
            src_words = len(article.split())
            lang = detect(article)
            st.markdown(f'<span class="chip">🌐 {html.escape(lang)}</span>'
                        f'<span class="chip">📝 {src_words} words</span>', unsafe_allow_html=True)
            if lang == "English":
                st.info("This tool is built and tested for Hindi, Bengali and code-mixed text. "
                        "English input works, but results are outside the study.")
            col1, col2 = st.columns(2)
            panels = [(col1, "standard", "Standard prompt", "🤖"),
                      (col2, "factual", "Factuality-aware prompt", "🛡️")]
            avgs = {}
            for col, mode, title, icon in panels:
                with col:
                    with st.spinner(f"{title}: summarizing..."):
                        summary, secs = summarize(article, mode)
                    if clean_on:
                        summary = strip_preamble(summary)
                    with st.spinner(f"{title}: checking facts..."):
                        scored = score_summary(article, summary)
                    if skip_short:
                        scored = [(s, sc) for s, sc in scored if len(s.split()) >= 4]
                    words = len(summary.split())
                    st.markdown(f'<div class="card"><h3>{icon} {title}</h3>'
                                f'<div>{html.escape(summary).replace(chr(10), "<br>")}</div></div>',
                                unsafe_allow_html=True)
                    st.markdown(f'<span class="chip">⏱ {secs} sec</span>'
                                f'<span class="chip">📏 {words} words</span>'
                                f'<span class="chip">🗜 compression {words / src_words:.2f}</span>',
                                unsafe_allow_html=True)
                    if scored:
                        avg = sum(sc for _, sc in scored) / len(scored)
                        avgs[mode] = avg
                        sup = sum(1 for _, sc in scored if sc >= 0.5)
                        st.markdown(gauge(avg, sup, len(scored)), unsafe_allow_html=True)
                        for sent, sc in scored:
                            st.markdown(f'<div class="sent s-{band(sc)}"><span class="sc">{sc:.2f}</span>'
                                        f'{html.escape(sent)}</div>', unsafe_allow_html=True)
                    else:
                        st.info("No sentences long enough to score.")
            if len(avgs) == 2:
                d = avgs["factual"] - avgs["standard"]
                if abs(d) < 0.03:
                    st.markdown('<div class="winner tie">🤝 Both prompts scored about the same on this article.</div>',
                                unsafe_allow_html=True)
                else:
                    w = "Factuality-aware prompt" if d > 0 else "Standard prompt"
                    st.markdown(f'<div class="winner">🏆 {w} scored higher on this article '
                                f'(difference {abs(d):.2f}).</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Final results from the study (20 articles per dataset)")
    try:
        df = pd.read_csv("results/FINAL_table.csv")
        df["setting"] = df["dataset"] + " / " + df["method"]
        show = df[["dataset", "method", "avg_summary_words", "compression_ratio", "avg_time_sec",
                   "pct_sentences_supported", "fact_precision", "rouge1_F1", "bert_F1"]]
        st.dataframe(show, use_container_width=True, hide_index=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**NLI: % of sentences supported**")
            st.bar_chart(df.pivot(index="dataset", columns="method", values="pct_sentences_supported"))
        with c2:
            st.markdown("**BERTScore F1**")
            st.bar_chart(df.pivot(index="dataset", columns="method", values="bert_F1"))
        st.caption("Small sample (20 per dataset): read gaps as trends, not proof. Timing is noisy.")
    except Exception as e:
        st.info("Results table not found. Run final_table.py first. (" + str(e) + ")")

st.markdown("---")
st.caption("FactIndic · CSET 346 NLP project · scores are automatic estimates, not guarantees.")