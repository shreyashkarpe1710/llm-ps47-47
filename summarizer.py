"""Weekly/monthly summaries and Ask-My-Journal chat (Gemini with extractive fallback)."""
import os
SUMMARY_PROMPT = """You are a supportive journal reviewer. Given these entries with mood scores: {data}
Write a {period} summary with: 1) Overall mood trend 2) 3 highlights 3) 2 difficult moments
4) Repeated topics/tags 5) One gentle, practical suggestion for next week.
Under 220 words, simple English, no medical advice."""
CHAT_PROMPT = """Answer the question using ONLY these journal entries: {context}
Question: {q}
If the answer is not in the entries, say: I could not find that in your journal."""
def fallback_summary(df, period="weekly"):
    avg = round(float(df["mood_score"].mean()),2); best=df.loc[df["mood_score"].idxmax()]; worst=df.loc[df["mood_score"].idxmin()]
    return (f"Overall mood trend ({period}): average mood {avg}/5 across {len(df)} entries. "
            f"Highlights: best day {best['date']} ({best['mood_label']}, {best['mood_score']}). "
            f"Difficult moment: {worst['date']} ({worst['mood_label']}, {worst['mood_score']}). "
            f"Suggestion: protect sleep and take a short walk on low-mood days.")
def summarise(df, period="weekly"):
    key=os.getenv("GEMINI_API_KEY","")
    if key:
        try:
            import google.generativeai as genai; genai.configure(api_key=key)
            m=genai.GenerativeModel("gemini-2.0-flash")
            return m.generate_content(SUMMARY_PROMPT.format(data=df.to_dict("records"), period=period)).text
        except Exception: pass
    return fallback_summary(df, period)
def ask_journal(df, question):
    hits = df[df["entry"].str.contains(question.split()[0], case=False, na=False)] if question.split() else df
    rows = hits if not hits.empty else df.tail(3)
    return "Based on your journal: " + " | ".join(f"{r['date']}: {r['entry']}" for _,r in rows.iterrows())
