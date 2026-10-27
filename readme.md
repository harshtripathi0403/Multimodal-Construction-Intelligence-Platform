# BuildSight AI - Multimodal Construction Intelligence Platform

BuildSight AI is a Streamlit capstone application for construction planning and daily site-support workflows. It delivers a transparent, deployable demonstration of the platform requirements without using a paid API key or database.

## Features

- **Safety & PPE audit:** records a site observation, a manual PPE verification checklist, priority controls, and a downloadable JSON report.
- **Crack diagnostics:** records material, an observed crack width, safe next steps, and a downloadable JSON observation report.
- **Planning & valuation:** estimates construction budget, capital spent, illustrative market value, cement, and steel indicators in INR.
- **Daily site assistant:** provides weather-aware operational prompts and an educational construction guidance assistant.
- **Multimodal inputs:** accepts JPG/PNG site and surface images; image metadata is included in reports and images are not persisted by the app.

## Safety and scope

This is a capstone demonstration, not a computer-vision safety system, structural diagnosis tool, quantity survey, or property valuation. It labels all generated outputs accordingly. A qualified safety professional, structural engineer, quantity surveyor, and local authority must validate actual site decisions.

## Run locally

```powershell
cd construction-intelligence
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Put the `construction-intelligence` folder contents in a public GitHub repository, or set the Streamlit main file path to `construction-intelligence/app.py`.
2. In Streamlit Community Cloud, choose **New app**, select the repository and the `main` branch.
3. Set the main file to `construction-intelligence/app.py` (or `app.py` if the folder contents are placed at the repository root).
4. Deploy, then submit both the public GitHub link and the generated `streamlit.app` link on SkillWallet.

## Technology

- Python and Streamlit
- Pillow and NumPy for local image metadata
- Pandas for tabular reports and charts
- JSON data contracts for reports
