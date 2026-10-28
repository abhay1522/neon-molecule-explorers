# Cheminformatics Virtual Laboratory (Neon / Molecular theme)

Streamlit + RDKit app by **Abhay Raj** – B.Tech CSE (AI/ML), Section C,
SRM Institute of Science and Technology, Tiruchirappalli.

## Files
| File | Purpose |
|---|---|
| app.py | Entry point: page config, sidebar navigation, routing |
| ui_helpers.py | Neon CSS theme, sidebar, 3D viewer, **your name/details (edit here)** |
| chem_utils.py | RDKit functions: parsing, descriptors, 2D/3D, bond counts |
| lab_pages.py | All 7 pages (Home, Theory, Visualization, Report, Analysis, Assessment, Final Report) |
| report_utils.py | PDF report generation (ReportLab) |
| requirements.txt | Python packages |
| packages.txt | System packages for Streamlit Cloud |
| .streamlit/config.toml | Dark theme colours |
| README.md | This file |

## Run locally
    pip install -r requirements.txt
    streamlit run app.py

## Deploy
Upload all files to a GitHub repo (keep the `.streamlit` folder), then create the app on share.streamlit.io with main file `app.py`.
