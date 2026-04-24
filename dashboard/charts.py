import hashlib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

MERCHANT_CATEGORIES = [
    "Groceries & Supermarkets",
    "Restaurants & Dining",
    "Gas & Transportation",
    "Healthcare & Pharmacy",
    "Shopping & Retail",
    "Entertainment",
    "Travel & Hotels",
    "Utilities & Services",
]

PALETTE = px.colors.qualitative.Pastel


def _merchant_category(merchant_id: str) -> str:
    h = int(hashlib.md5(merchant_id.encode()).hexdigest(), 16)
    return MERCHANT_CATEGORIES[h % len(MERCHANT_CATEGORIES)]


def _loan_type(amount: float) -> str:
    if amount < 25_000:
        return "Personal"
    if amount < 100_000:
        return "Auto"
    return "Mortgage"


def ttv_bar(accounts: pd.DataFrame) -> go.Figure:
    df = accounts.groupby("account_type")["balance_usd"].sum().reset_index()
    df.columns = ["Account Type", "Total Balance (USD)"]
    fig = px.bar(
        df,
        x="Account Type",
        y="Total Balance (USD)",
        color="Account Type",
        text_auto=".3s",
        color_discrete_sequence=PALETTE,
        title="Total Transaction Volume by Account Type",
    )
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="USD")
    fig.update_traces(textposition="outside")
    return fig


def merchant_donut(merchants: pd.DataFrame) -> go.Figure:
    df = merchants.copy()
    df["Category"] = df["merchant_id"].apply(_merchant_category)
    counts = df.groupby("Category").size().reset_index(name="Merchants")
    fig = px.pie(
        counts,
        names="Category",
        values="Merchants",
        hole=0.5,
        color_discrete_sequence=PALETTE,
        title="Spending Distribution by Merchant Category",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False)
    return fig


def atv_hbar(accounts: pd.DataFrame) -> go.Figure:
    df = accounts.groupby("account_type")["balance_usd"].mean().reset_index()
    df.columns = ["Account Type", "Avg Balance (USD)"]
    fig = px.bar(
        df,
        x="Avg Balance (USD)",
        y="Account Type",
        orientation="h",
        color="Account Type",
        text_auto=".3s",
        color_discrete_sequence=PALETTE,
        title="Average Transaction Value by Account Type",
    )
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title="USD")
    fig.update_traces(textposition="outside")
    return fig


def loan_exposure_treemap(loans: pd.DataFrame) -> go.Figure:
    df = loans.copy()
    df["Loan Type"] = df["loan_amount"].apply(_loan_type)
    df["Rate Tier"] = pd.cut(
        df["interest_rate"],
        bins=[0, 5, 10, 100],
        labels=["Low (<5%)", "Mid (5–10%)", "High (>10%)"],
    ).astype(str)
    agg = (
        df.groupby(["Loan Type", "Rate Tier"])["loan_amount"]
        .sum()
        .reset_index()
    )
    agg.columns = ["Loan Type", "Rate Tier", "Exposure (USD)"]
    fig = px.treemap(
        agg,
        path=["Loan Type", "Rate Tier"],
        values="Exposure (USD)",
        color="Exposure (USD)",
        color_continuous_scale="Blues",
        title="Total Active Loan Exposure",
    )
    fig.update_traces(texttemplate="<b>%{label}</b><br>$%{value:,.0f}")
    return fig


def weighted_rate_bar(loans: pd.DataFrame) -> go.Figure:
    df = loans.copy()
    df["Loan Type"] = df["loan_amount"].apply(_loan_type)
    agg = (
        df.assign(weighted_interest=df["interest_rate"] * df["loan_amount"])
        .groupby("Loan Type")
        .agg(total_weighted=("weighted_interest", "sum"), total_amount=("loan_amount", "sum"))
        .assign(**{"Weighted Rate (%)": lambda d: d["total_weighted"] / d["total_amount"]})
        .reset_index()[["Loan Type", "Weighted Rate (%)"]]
    )
    fig = px.bar(
        agg,
        x="Loan Type",
        y="Weighted Rate (%)",
        color="Loan Type",
        text_auto=".2f",
        color_discrete_sequence=PALETTE,
        title="Weighted Average Interest Rate by Loan Type",
    )
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Rate (%)")
    fig.update_traces(texttemplate="%{y:.2f}%", textposition="outside")
    return fig
