"""Analytics for the major version: weekly/monthly stats, streaks, distribution."""
import pandas as pd
def to_df(rows): 
    df = pd.DataFrame(rows); 
    return df
def weekly_stats(df):
    if df.empty or "mood_score" not in df: return {}
    return {"count": int(len(df)), "average_mood": round(float(df["mood_score"].mean()),2),
            "best_day": df.loc[df["mood_score"].idxmax()].to_dict(),
            "worst_day": df.loc[df["mood_score"].idxmin()].to_dict(),
            "positive_days": int((df["mood_score"]>0).sum()), "negative_days": int((df["mood_score"]<0).sum())}
def mood_distribution(df):
    return df["mood_label"].value_counts().to_dict() if not df.empty and "mood_label" in df else {}
def current_streak(df):
    """Consecutive days (by row order on distinct dates) with an entry."""
    if df.empty: return 0
    dates = sorted(pd.to_datetime(df["date"]).dt.date.unique()); streak=1
    for i in range(len(dates)-1,0,-1):
        if (dates[i]-dates[i-1]).days==1: streak+=1
        else: break
    return streak
def monthly_average(df):
    if df.empty: return {}
    d=df.copy(); d["month"]=pd.to_datetime(d["date"]).dt.strftime("%Y-%m")
    return d.groupby("month")["mood_score"].mean().round(2).to_dict()
