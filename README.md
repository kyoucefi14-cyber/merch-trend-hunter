# Merch Trend Hunter — Starter v0.1

Bilingual (English/Arabic) Streamlit starter dashboard for researching US print-on-demand opportunities.

## Important
The current rows are illustrative demo data. They are NOT live Google Trends data, Amazon search results, verified BSR, or actual sales.

## Run locally
```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy
1. Create a GitHub repository named `merch-trend-hunter`.
2. Upload the files from this project.
3. Open https://share.streamlit.io and sign in with GitHub.
4. Create app; select your repository, branch `main`, and file `streamlit_app.py`.
5. Deploy.

## Planned architecture
- Web UI: Streamlit Community Cloud
- Source control: GitHub
- Database: Supabase/Postgres (after account and schema setup)
- Scheduled collector: GitHub Actions or a separate scheduled worker
- Data sources: official/authorized APIs and public sources with permitted access
- Amazon research: permitted methods only; no bypassing bot controls or restricted access.

## Next milestones
1. Deploy this starter.
2. Create a persistent database.
3. Add a collector for one trend source and store timestamped observations.
4. Add Amazon competition observations.
5. Add risk screening for trademarks/copyright and platform policies.
6. Add alerting and opportunity history.
