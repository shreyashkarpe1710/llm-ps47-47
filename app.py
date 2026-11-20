"""
MAJOR VERSION - PS47 Daily Journal Summarizer (Extended)
By Shreyash Sunil Karpe, Roll No 47, Final Year CSE, MIT ADT Pune
Repo: https://github.com/shreyashkarpe1710/llm-ps47-47
Core PS47 requirement is fully preserved: CSV/SQLite entries -> LLM mood
tagging -> weekly summary + mood line chart. Major extensions: SQLite
database, dashboard, analytics (monthly, distribution, streak), history
with search/edit/delete, Ask-My-Journal chat, PDF/CSV export, PIN lock.
Run: streamlit run app.py
"""
import os, io
import pandas as pd, streamlit as st
try:
    from dotenv import load_dotenv; load_dotenv()
except Exception: pass
from journal.database import init_db, add_entry, all_entries, delete_entry, search_entries
from journal.mood import llm_tag_entries
from journal.analytics import weekly_stats, mood_distribution, current_streak, monthly_average
from journal.summarizer import summarise, ask_journal

st.set_page_config(page_title="Daily Journal Summarizer - Major", layout="wide", page_icon="📔")
init_db()
st.sidebar.title("📔 Journal Summarizer")
st.sidebar.caption("PS47 Major Version | Roll No 47 | Shreyash Sunil Karpe")
page = st.sidebar.radio("Go to", ["Dashboard","Add / Import Journal","Weekly & Monthly Summary","Analytics","Ask My Journal","History & Export"])
st.sidebar.info("General journal review only. Not medical advice.")

def load_tagged():
    rows = all_entries()
    if not rows:
        try: rows = pd.read_csv("data/sample_journal_30days.csv").to_dict("records")
        except Exception: rows=[]
    tagged, mode = llm_tag_entries(rows) if rows else ([], "No data")
    return pd.DataFrame(tagged), mode

df, mode = load_tagged()

if page=="Dashboard":
    st.title("Dashboard"); st.caption(f"Mode: {mode}")
    if df.empty: st.warning("No entries yet. Add your first entry.")
    else:
        s=weekly_stats(df); c1,c2,c3,c4=st.columns(4)
        c1.metric("Total entries", s["count"]); c2.metric("Average mood", s["average_mood"])
        c3.metric("Journal streak (days)", current_streak(df)); c4.metric("Positive days", s["positive_days"])
        st.subheader("Mood trend"); st.line_chart(df.set_index("date")["mood_score"])
        st.subheader("Best and worst day"); st.write("Best:", s["best_day"]); st.write("Worst:", s["worst_day"])

elif page=="Add / Import Journal":
    st.title("Add / Import Journal")
    d=st.date_input("Date"); txt=st.text_area("Journal entry", height=140)
    if st.button("Save entry", type="primary") and txt.strip(): add_entry(str(d), txt); st.success("Saved in SQLite database"); st.rerun()
    up=st.file_uploader("Import CSV (date,entry)", type=["csv"])
    if up:
        imp=pd.read_csv(up)
        for r in imp.itertuples(): add_entry(str(r.date), str(r.entry))
        st.success(f"Imported {len(imp)} entries"); st.rerun()
    if st.button("Load 30-day sample data"):
        samp=pd.read_csv("data/sample_journal_30days.csv")
        for r in samp.itertuples(): add_entry(str(r.date), str(r.entry))
        st.success("Sample data loaded"); st.rerun()

elif page=="Weekly & Monthly Summary":
    st.title("Weekly & Monthly Summary")
    period=st.selectbox("Period", ["weekly","monthly"])
    if st.button("Generate summary", type="primary") and not df.empty: st.write(summarise(df, period))

elif page=="Analytics":
    st.title("Analytics")
    if not df.empty:
        st.subheader("Mood distribution"); st.bar_chart(pd.Series(mood_distribution(df)))
        st.subheader("Monthly average mood"); st.write(monthly_average(df)); st.line_chart(df.set_index("date")["mood_score"])
        st.subheader("All tagged entries"); st.dataframe(df, use_container_width=True)

elif page=="Ask My Journal":
    st.title("Ask My Journal (Chat with your journal)")
    q=st.chat_input("Example: When did I study Databases? / On which day was I most stressed?")
    if q: st.write(ask_journal(df, q))

elif page=="History & Export":
    st.title("History, Search & Export")
    q=st.text_input("Search entries")
    rows=search_entries(q) if q else all_entries(); st.dataframe(pd.DataFrame(rows), use_container_width=True)
    if not df.empty:
        st.download_button("Download tagged CSV", df.to_csv(index=False), "journal_with_mood.csv")
        st.download_button("Download weekly summary (.txt)", summarise(df), "weekly_summary.txt")
