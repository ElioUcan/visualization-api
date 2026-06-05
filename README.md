# Financial KPI Dashboard

## 🛠️ Technologies
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## ✨ Features
- 5 interactive financial KPI charts: Total Transaction Volume, Spending Distribution, Average Transaction Value, Loan Exposure treemap, and Weighted Average Interest Rate
- CSV-to-PostgreSQL loader that creates tables, adds primary keys, and inserts rows in dependency order
- Loan classification by amount: Personal (< $25K), Auto ($25K–$100K), Mortgage (> $100K)
- Relational banking dataset: accounts, branches, cards, customers, loans, and merchants

## 🎯 Uses
Collaborative financial dashboard exploring a synthetic banking dataset with KPI visualizations. Built as a university group project to demonstrate data loading, relational data modeling, and interactive business intelligence charts.

## 🔧 Process
The `load_csv_to_db.py` script loads six CSV files into PostgreSQL, inferring table schemas from headers and adding foreign-key relationships in the correct dependency order. The Streamlit dashboard (`dashboard/app.py`) queries the database and builds Plotly charts for each KPI. The two components are decoupled — run the loader once, then the dashboard independently.

## 💡 Learnings
- Designing KPI metrics from raw banking data requires understanding the domain: loan classification by amount, weighted interest rates, and merchant category inference
- Treemaps communicate hierarchical financial exposure (loan type → interest rate tier) more effectively than flat bar charts
- Decoupling the data loader from the dashboard makes it easy to refresh data without restarting the UI

## ▶️ Running the project

```bash
pip install -r requirements.txt

# Load data into PostgreSQL (once)
cp .env.example .env  # fill in DB credentials
python scripts/load_csv_to_db.py

# Start the dashboard
streamlit run dashboard/app.py
```

Open **http://localhost:8501** in your browser.
