"""Mood tagging: Gemini LLM first, keyword Demo Mode as reliable fallback."""
import os, json, re
MOOD_PROMPT = """You are a journal analysis assistant. For each journal entry below,
return ONLY a JSON list. Each item: date, mood_label
(Positive/Stressed/Anxious/Calm/Neutral), mood_score (integer -5 to +5),
highlight (one short line), tags (list of up to 3 topic tags).
Entries:\n{entries}\nReturn only JSON, no extra text."""
POS = ["happy","focused","good","great","proud","excited","calm","peaceful","motivated","satisfied","relaxed","well","progress","completed","solved"]
NEG = ["stressed","tired","anxious","distracted","poor","worried","sad","angry","failed","difficult","pressure"]
def demo_tag(text):
    t = text.lower()
    s = sum(1 for w in POS if w in t) - sum(1 for w in NEG if w in t)
    s = max(-5, min(5, s*2))
    label = "Positive" if s>=2 else "Stressed" if s<=-3 else "Anxious" if "anxious" in t else "Neutral" if s==0 else "Calm"
    if "stressed" in t: label="Stressed"
    tags = [w for w in ["study","gate","placement","project","walk","sleep","team","exam"] if w in t][:3]
    return label, int(s), tags
def llm_tag_entries(rows):
    """rows: list of dicts with date, entry. Returns (tagged_rows, mode)."""
    key = os.getenv("GEMINI_API_KEY","")
    if not key:
        out=[]
        for r in rows:
            label,score,tags = demo_tag(r["entry"])
            out.append({**r,"mood_label":label,"mood_score":score,"highlight":r["entry"][:70],"tags":tags})
        return out, "Demo Mode (no API key)"
    try:
        import google.generativeai as genai
        genai.configure(api_key=key); model = genai.GenerativeModel("gemini-2.0-flash")
        entries = "\n".join(f"{r['date']}: {r['entry']}" for r in rows)
        txt = model.generate_content(MOOD_PROMPT.format(entries=entries)).text
        data = json.loads(re.search(r"\[.*\]", txt, re.S).group())
        by = {d["date"]: d for d in data}
        return [{**r, **by.get(r["date"], {})} for r in rows], "Gemini LLM Mode"
    except Exception as e:
        tagged,_ = llm_tag_entries.__wrapped__(rows) if hasattr(llm_tag_entries,"__wrapped__") else (None,None)
        out=[]
        for r in rows:
            label,score,tags = demo_tag(r["entry"]); out.append({**r,"mood_label":label,"mood_score":score,"highlight":r["entry"][:70],"tags":tags})
        return out, f"Demo Mode (LLM fallback: {e})"
