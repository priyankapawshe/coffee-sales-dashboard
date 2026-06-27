# ============================================================
# app.py — Afficionado Coffee Roasters Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config (must be FIRST streamlit command) ---
st.set_page_config(
    page_title="Coffee Roasters Dashboard",
    page_icon="☕",
    layout="wide"
)

# --- Load Data ---
@st.cache_data   # This caches the data so it doesn't reload every time
def load_data():
    df = pd.read_csv("data/transactions.csv")
    df["revenue"] = df["transaction_qty"] * df["unit_price"]
    df["hour"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S").dt.hour
    return df

df = load_data()

# --- Header ---
st.title("☕ Afficionado Coffee Roasters")
st.markdown("### Sales Performance Dashboard")
st.divider()

# --- KPI Cards (top row) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",      f"${df['revenue'].sum():,.0f}")
col2.metric("Total Transactions", f"{len(df):,}")
col3.metric("Avg Order Value",    f"${df['revenue'].mean():.2f}")
col4.metric("Unique Products",    f"{df['product_detail'].nunique()}")

st.divider()

# --- Sidebar filters ---
st.sidebar.header("Filters")
stores = ["All Stores"] + list(df["store_location"].unique())
selected_store = st.sidebar.selectbox("Select Store", stores)

categories = ["All Categories"] + list(df["product_category"].unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Apply filters
filtered = df.copy()
if selected_store != "All Stores":
    filtered = filtered[filtered["store_location"] == selected_store]
if selected_category != "All Categories":
    filtered = filtered[filtered["product_category"] == selected_category]

# --- Row 1: Store Revenue & Category Breakdown ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue by Store")
    store_rev = filtered.groupby("store_location")["revenue"].sum().reset_index()
    fig1 = px.bar(
        store_rev, x="store_location", y="revenue",
        color="store_location",
        labels={"store_location": "Store", "revenue": "Revenue ($)"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(showlegend=False, margin=dict(t=10))
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Revenue by Category")
    cat_rev = filtered.groupby("product_category")["revenue"].sum().reset_index()
    fig2 = px.pie(
        cat_rev, names="product_category", values="revenue",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig2.update_layout(margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

# --- Row 2: Hourly trend & Top products ---
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Sales by Hour of Day")
    hourly = filtered.groupby("hour")["revenue"].sum().reset_index()
    fig3 = px.line(
        hourly, x="hour", y="revenue",
        markers=True,
        labels={"hour": "Hour (24h)", "revenue": "Revenue ($)"}
    )
    fig3.update_layout(margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("Top 10 Products")
    top_products = (
        filtered.groupby("product_detail")["revenue"]
        .sum().sort_values(ascending=True)
        .tail(10).reset_index()
    )
    fig4 = px.bar(
        top_products, x="revenue", y="product_detail",
        orientation="h",
        labels={"product_detail": "Product", "revenue": "Revenue ($)"},
        color="revenue",
        color_continuous_scale="Blues"
    )
    fig4.update_layout(margin=dict(t=10), showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# --- Raw Data Table (expandable) ---
with st.expander("View Raw Data"):
    st.dataframe(filtered.head(500), use_container_width=True)

st.caption("Data source: Afficionado Coffee Roasters Transactions")
