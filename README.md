# Daily Journal Summarizer - PS47

**GenAI (LLM) Mini Project extended to a full project**
**Name:** Shreyash Sunil Karpe | **Roll No:** 47 | **Problem Statement:** 47
**Class:** Final Year CSE, MIT ADT University, Pune
**GitHub:** https://github.com/shreyashkarpe1710/llm-ps47-47

## Repository Description
PS47 Daily Journal Summarizer - a Streamlit app that stores daily journal entries, uses the Gemini LLM to tag mood for each entry, shows weekly and monthly mood trends with charts, and generates a weekly summary with highlights.

## Problem Statement (from the allotted PDF)
Journaling without review has little value. Summarise weekly journal entries into mood trends and highlights.
How to solve (from PDF): Store entries in a CSV with dates -> LLM tags mood per entry -> weekly summary + a line chart of mood. This project implements exactly that, and extends it with a database, dashboard, analytics and a journal chat.

## Features
1. **Dashboard** - total entries, average mood, journal streak, positive days, best/worst day, mood trend chart
2. **Add / Import Journal** - add an entry, import CSV (date,entry), or load the 30-day sample data; stored in SQLite
3. **Weekly & Monthly Summary** - Gemini LLM summary with highlights, difficult moments and a suggestion
4. **Analytics** - mood distribution, monthly average mood, topic tags, full tagged table
5. **Ask My Journal** - ask questions answered only from your own entries
6. **History & Export** - search entries, download tagged CSV and summary text
7. **Demo Mode** - if no Gemini API key is available, a keyword mood scorer runs so the demo never fails

## Project Structure
```
app.py                  Main Streamlit app (6 pages via sidebar)
journal/database.py     SQLite storage (add, view, search, delete)
journal/mood.py         LLM mood tagging prompt + Demo Mode fallback
journal/analytics.py    Weekly/monthly stats, streak, distribution
journal/summarizer.py   Weekly/monthly summary + Ask-My-Journal
journal/utils.py        Small helpers
data/sample_journal.csv             7-day sample (PS47 core test data)
data/sample_journal_30days.csv      30-day sample dataset
tests/test_project.py   Unit tests (mood tagging and analytics)
screenshots/            Output screenshots
requirements.txt
```

## How to Run
```
pip install -r requirements.txt
streamlit run app.py
```
Optional: create a `.env` file with `GEMINI_API_KEY=your_free_key` (from Google AI Studio) for full LLM mode. Never upload `.env` to GitHub - it is blocked by `.gitignore`.

## Prompt Used
Mood prompt: "You are a journal analysis assistant. For each entry return ONLY a JSON list with date, mood_label (Positive/Stressed/Anxious/Calm/Neutral), mood_score (-5 to +5), highlight and tags."
Improvement: added "Return only JSON, no extra text" after the first version returned extra explanation and JSON parsing failed.

## Testing
Tested on 30 sample entries (22 Oct - 20 Nov 2026). Average mood 1.53/5, Positive 20, Stressed 8, Calm 1, Anxious 1. Unit tests in `tests/` pass.

## Note
This app gives a general journal review only. It is not medical advice.
