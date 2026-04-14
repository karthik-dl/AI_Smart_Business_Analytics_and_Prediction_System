#  Smart Business Analytics & Prediction System

## What does this app do?

This is a web-based analytics tool built with Python and Streamlit.  
You upload a CSV file containing your business data, and the app automatically:

- Shows you a **preview** of your data
- Trains a **machine learning model** to predict future Sales
- Displays a **live dashboard** with charts, KPIs, and filters
- Forecasts **what sales will look like in the next 3 months**
- Detects **anomalies** — unusual rows that don't match normal patterns
- Compares **multiple ML models** to find the best one for your data
- Generates a **downloadable PDF report**
- Writes **AI text insights** describing what the data shows

---

## How to run it

### Step 1 — Install Python
Make sure you have **Python 3.9 or higher** installed.  
Check your version by running: `python --version`

### Step 2 — Install dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```
This installs all the libraries the app needs (Streamlit, Pandas, Plotly, etc.)

### Step 3 — Start the app
```bash
streamlit run app.py
```
Your browser will automatically open at `http://localhost:8501`


## What CSV file should I upload?

Your CSV file should have columns like these:

| Column name | Type    | Required? | What it means                        |
|-------------|---------|-----------|--------------------------------------|
| `Sales`     | number  | Yes       | The sales value for each row         |
| `Profit`    | number  | No        | The profit value for each row        |
| `Region`    | text    | No        | Geographic area (e.g. North, West)   |
| `Category`  | text    | No        | Product or service type              |
| Date column | date    | No        | Used for monthly forecasting charts  |

> If a column is missing, the app will simply skip the feature that needs it — nothing will crash.

---

## Project folder structure

```
project/
│
├── app.py                   ← The main file. Run this to start the app.
├── requirements.txt         ← List of Python packages to install.
├── README.md                ← This file. Explains how everything works.
├── .gitignore               ← Tells Git which files NOT to track (model.pkl, .env, etc.)
├── model.pkl                ← The saved ML model (created after you click "Train Model")
│
└── src/                     ← All the helper modules. Each file has one job.
    │
    ├── preprocessing.py     ← Reads the CSV and cleans the data (fix nulls, fix types)
    ├── model.py             ← Trains the Random Forest model and saves/loads model.pkl
    ├── model_comparison.py  ← Tests multiple ML models and compares their accuracy
    ├── forecasting.py       ← Predicts sales for the next 3 months using past trends
    ├── anomaly_detection.py ← Finds rows that look unusual compared to the rest
    ├── visualization.py     ← Builds the 3 charts: by region, by month, by category
    ├── insights.py          ← Generates AI-written text observations about the data
    └── report_generator.py  ← Creates the downloadable PDF business report
```

---

## Tech stack — what each library does

| Library       | What it does in this project                              |
|---------------|-----------------------------------------------------------|
| `streamlit`   | Builds the entire web UI — buttons, charts, tables, etc.  |
| `pandas`      | Reads the CSV and lets us work with the data as a table   |
| `numpy`       | Fast number crunching used by the ML model                |
| `scikit-learn`| Provides the Random Forest model and other ML algorithms  |
| `statsmodels` | Powers the sales forecasting feature                      |
| `joblib`      | Saves the trained model to model.pkl and loads it back    |
| `plotly`      | Creates the interactive charts in the dashboard           |
| `matplotlib`  | Used internally by some modules for basic charts          |
| `seaborn`     | Used internally for styled statistical charts             |
| `reportlab`   | Generates the downloadable PDF report                     |