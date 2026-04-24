from pathlib import Path

import pandas as pd
import streamlit as st

from charts import atv_hbar, loan_exposure_treemap, merchant_donut, ttv_bar, weighted_rate_bar

DATA_DIR = Path(__file__).parent.parent / "data"

st.set_page_config(page_title="Financial KPI Dashboard", layout="wide")


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    accounts = pd.read_csv(DATA_DIR / "accounts.csv")
    accounts["balance_usd"] = pd.to_numeric(accounts["balance_usd"], errors="coerce")

    loans = pd.read_csv(DATA_DIR / "loans.csv")
    loans["loan_amount"] = pd.to_numeric(loans["loan_amount"], errors="coerce")
    loans["interest_rate"] = pd.to_numeric(loans["interest_rate"], errors="coerce")

    merchants = pd.read_csv(DATA_DIR / "merchants.csv")
    return accounts, loans, merchants


accounts, loans, merchants = load_data()

ttv = accounts["balance_usd"].sum()
loan_exposure = loans["loan_amount"].sum()
weighted_rate = (
    (loans["interest_rate"] * loans["loan_amount"]).sum() / loans["loan_amount"].sum()
)
avg_balance = accounts["balance_usd"].mean()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Financial KPI Dashboard")
st.caption(
    "TTV and ATV are derived from account balances. "
    "Merchant categories are inferred; loan types are classified by amount."
)

# ── KPI metric cards ──────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Transaction Volume", f"${ttv:,.0f}")
m2.metric("Total Active Loan Exposure", f"${loan_exposure:,.0f}")
m3.metric("Weighted Avg Interest Rate", f"{weighted_rate:.2f}%")
m4.metric("Avg Transaction Value", f"${avg_balance:,.0f}")

st.divider()

# ── Row 1: TTV bar + Merchant donut ──────────────────────────────────────────
r1a, r1b = st.columns([3, 2])
with r1a:
    st.plotly_chart(ttv_bar(accounts), use_container_width=True)
with r1b:
    st.plotly_chart(merchant_donut(merchants), use_container_width=True)

# ── Row 2: ATV horizontal bar + Weighted rate bar ────────────────────────────
r2a, r2b = st.columns(2)
with r2a:
    st.plotly_chart(atv_hbar(accounts), use_container_width=True)
with r2b:
    st.plotly_chart(weighted_rate_bar(loans), use_container_width=True)

# ── Row 3: Loan exposure treemap (full width) ─────────────────────────────────
st.plotly_chart(loan_exposure_treemap(loans), use_container_width=True)
