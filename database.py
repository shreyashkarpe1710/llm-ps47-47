"""SQLite storage - major version replaces CSV-only storage (CSV import/export is still supported)."""
import sqlite3, pathlib
DB = pathlib.Path(__file__).parent.parent/"data"/"journal.db"
def connect():
    DB.parent.mkdir(exist_ok=True); con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; return con
def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS entries(
          id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, entry TEXT NOT NULL,
          mood_label TEXT, mood_score INTEGER, highlight TEXT, tags TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pin_hash TEXT)""")
def add_entry(date, entry, mood_label=None, mood_score=None, highlight=None, tags=""):
    init_db()
    with connect() as c: cur=c.execute("INSERT INTO entries(date,entry,mood_label,mood_score,highlight,tags) VALUES(?,?,?,?,?,?)",(date,entry,mood_label,mood_score,highlight,tags)); return cur.lastrowid
def all_entries():
    init_db()
    with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM entries ORDER BY date")]
def update_entry(eid, entry):
    with connect() as c: c.execute("UPDATE entries SET entry=? WHERE id=?",(entry,eid))
def delete_entry(eid):
    with connect() as c: c.execute("DELETE FROM entries WHERE id=?",(eid,))
def search_entries(q):
    init_db()
    with connect() as c: return [dict(r) for r in c.execute("SELECT * FROM entries WHERE entry LIKE ? ORDER BY date", (f"%{q}%",))]
