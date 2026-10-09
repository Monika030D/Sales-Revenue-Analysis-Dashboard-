# Sales & Revenue Analysis Dashboard

Built with Python, Streamlit and Pandas.

## Features
- CSV import
- Total revenue, units, transactions and average transaction KPIs
- Monthly revenue trend
- Top products
- Region and category analysis
- Interactive filters
- Sales data table
- Automatic business insights

## Run on Windows
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL, normally http://localhost:8501

## CSV columns
Date, Product, Category, City, Region, Quantity, Unit_Price, Revenue
