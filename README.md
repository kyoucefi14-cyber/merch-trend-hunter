# Merch Trend Hunter v0.2

Bilingual Streamlit dashboard and daily GitHub Actions collector.

## Data source
Google Trends US trending-searches RSS feed: `https://trends.google.com/trending/rss?geo=US`

## What this version does
- Collects currently listed US trending searches.
- Saves title, feed traffic label, publication date, related news URL, and collection timestamp.
- Displays the saved data in Streamlit.
- Runs daily at 13:00 UTC; can also be run manually from GitHub Actions.

## Limitations
Google Trends interest is not absolute search volume, product demand, or sales. This RSS feed is a current trending list, not a historical time series. This version does not provide verified growth, Amazon BSR, competition counts, or sales. Google's official Trends API remains limited alpha access.

## Install/update files
Upload these files to the existing repository, replacing same-named files:
- `streamlit_app.py`
- `collect_trends.py`
- `.github/workflows/daily-trends.yml`
- `data/trends.json`
- `requirements.txt`
- `README.md`
- `.streamlit/config.toml`

Then open GitHub Actions, enable workflows if prompted, select `Daily US Google Trends Collection`, and click `Run workflow` for the first test. After a successful run, `data/trends.json` will contain collected results and the Streamlit app will redeploy after the commit.

The schedule is 13:00 UTC (08:00 Eastern Standard Time / 09:00 Eastern Daylight Time).
