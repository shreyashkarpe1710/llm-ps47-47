from journal.mood import demo_tag
from journal.analytics import weekly_stats, current_streak
import pandas as pd
def test_positive(): 
    label,score,_=demo_tag("I felt happy and focused, completed my study"); assert label=="Positive" and score>0
def test_stressed():
    label,score,_=demo_tag("I felt stressed and tired, poor sleep"); assert score<0
def test_stats():
    df=pd.DataFrame([{"date":"2026-11-19","mood_score":5,"mood_label":"Positive"},{"date":"2026-11-20","mood_score":3,"mood_label":"Positive"}])
    assert weekly_stats(df)["average_mood"]==4.0 and current_streak(df)==2
