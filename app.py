# ============================================================================
# AFFICIONADO COFFEE ROASTERS - STREAMLIT DASHBOARD
# FULLY FIXED - With proper Excel engine handling
# ============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import sys

# --- Page config (must be FIRST streamlit command) ---
st.set_page_config(
    page_title="Coffee Roasters Dashboard",
    page_icon="☕",
    layout="wide"
)

# --- LOAD DATA FROM GITHUB ---
@st.cache_data
def load_data():
    """
    Load data from GitHub repository with multiple format support
    File: afficionado_coffee_cleaned_df_final.xls
    Repository: priyankapawshe/coffee-sales-dashboard
    """
    
    # YOUR GITHUB RAW FILE URLS - Try multiple versions
    github_urls = [
        # Primary: Direct .xls file
        "https://raw.githubusercontent.com/priyankapawshe/coffee-sales-dashboard/refs/heads/main/afficionado_coffee_cleaned_df_final.xls",
        # Alternative: Main branch syntax
        "https://raw.githubusercontent.com/priyankapawshe/coffee-sales-dashboard/main/afficionado_coffee_cleaned_df_final.xls",
        # Alternative: If converted to xlsx
        "https://raw.githubusercontent.com/priyankapawshe/coffee-sales-dashboard/refs/heads/main/afficionado_coffee_cleaned_df_final.xlsx",
        "https://raw.githubusercontent.com/priyankapawshe/coffee-sales-dashboard/main/afficionado_coffee_cleaned_df_final.xlsx",
    ]
    
    df = None
    loaded_url = None
    
    # Try each URL
    for github_url in github_urls:
        try:
            st.info(f"🔄 Trying to load from: {github_url.split('/')[-1]}")
            
            # Determine file type from URL
            if github_url.endswith('.xls'):
                # For .xls files - MUST specify engine='xlrd'
                df = pd.read_excel(github_url, engine='xlrd')
                loaded_url = github_url
                st.success(f"✅ Data loaded successfully from GitHub (.xls file)!")
                break
                
            elif github_url.endswith('.xlsx'):
                # For .xlsx files - specify engine='openpyxl'
                df = pd.read_excel(github_url, engine='openpyxl')
                loaded_url = github_url
                st.success(f"✅ Data loaded successfully from GitHub (.xlsx file)!")
                break
                
        except Exception as e:
            st.warning(f"⚠️ Could not load from {github_url.split('/')[-1]}: {str(e)[:100]}")
            continue
    
    # If GitHub URLs didn't work, try alternative method with requests
    if df is None:
        st.info("🔄 Trying alternative loading method with requests library...")
        
        try:
            import requests
            
            for github_url in github_urls:
                try:
                    response = requests.get(github_url)
                    response.raise_for_status()
                    
                    if github_url.endswith('.xls'):
                        df = pd.read_excel(io.BytesIO(response.content), engine='xlrd')
                    elif github_url.endswith('.xlsx'):
                        df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')
                    
                    loaded_url = github_url
                    st.success(f"✅ Data loaded successfully (via requests + {github_url.split('.')[-1]})!")
                    break
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            st.warning(f"⚠️ Alternative method failed: {str(e)[:100]}")
    
    # If still no data, show troubleshooting
    if df is None:
        st.error("""
        ❌ Could not load data from GitHub
        
        **Troubleshooting Steps:**
        
        1. **Check your GitHub repo is PUBLIC**
           - Go to Settings → Change visibility to Public
        
        2. **Verify file name is EXACT**
           - Should be: `afficionado_coffee_cleaned_df_final.xls`
           - No typos or extra spaces
        
        3. **Verify file location**
           - Should be in root folder of repo (not in subfolder)
        
        4. **Try these alternatives:**
        
        **Option A: Convert to CSV (Recommended - Easiest)**
        - Download your .xls file
        - Open in Excel
        - Save As → CSV format
        - Upload to GitHub as `coffee_data.csv`
        - Restart this app
        
        **Option B: Use Local File**
        - Download your .xls file
        - Place in same folder as app.py
        - Run: `streamlit run app.py`
        - App will use local file instead
        
        **Option C: Convert to XLSX**
        - Download your .xls file
        - Open in Excel
        - Save As → Excel 2007+ format (.xlsx)
        - Upload to GitHub
        - Restart this app
        
        **For CSV files:**
        - Works best with GitHub
        - Simplest to load
        - Recommended format
        """)
        return None
    
    if df is not None:
        st.success(f"📊 Loaded {len(df)} records from GitHub!")
        
        # Ensure required columns exist
        if 'revenue' not in df.columns and 'transaction_qty' in df.columns and 'unit_price' in df.columns:
            df['revenue'] = df['transaction_qty'] * df['unit_price']
        
        if 'hour' not in df.columns and 'transaction_time' in df.columns:
            try:
                df['hour'] = pd.to_datetime(df['transaction_time'], format='%H:%M:%S', errors='coerce').dt.hour
            except:
                try:
                    df['hour'] = pd.to_datetime(df['transaction_time'], errors='coerce').dt.hour
                except:
                    df['hour'] = 0
        
        if 'day_of_week' not in df.columns:
            df['day_of_week'] = 'Unknown'
        
        st.session_state['data_shape'] = df.shape
        st.session_state['data_loaded'] = True
        
    return df

# --- Load data ---
df = load_data()

if df is None:
    st.stop()

# --- HEADER ---
st.title("☕ Afficionado Coffee Roasters")
st.markdown("### Sales Performance Dashboard")

# Show data info
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.metric("📊 Total Records", f"{df.shape[0]:,}")
with col_info2:
    st.metric("📋 Columns", f"{df.shape[1]}")
with col_info3:
    st.metric("✅ Status", "Data Loaded")

st.divider()

# --- KPI CARDS (top row) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${df['revenue'].sum():,.0f}" if 'revenue' in df.columns else "N/A"
    )

with col2:
    st.metric(
        label="Total Transactions",
        value=f"{len(df):,}"
    )

with col3:
    st.metric(
        label="Avg Order Value",
        value=f"${df['revenue'].mean():.2f}" if 'revenue' in df.columns else "N/A"
    )

with col4:
    st.metric(
        label="Unique Products",
        value=f"{df['product_detail'].nunique()}" if 'product_detail' in df.columns else "N/A"
    )

st.divider()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔧 Filters")

# Store filter
if 'store_location' in df.columns:
    stores = ["All Stores"] + sorted(df["store_location"].unique().tolist())
    selected_store = st.sidebar.selectbox("📍 Select Store", stores)
else:
    selected_store = "All Stores"

# Category filter
if 'product_category' in df.columns:
    categories = ["All Categories"] + sorted(df["product_category"].unique().tolist())
    selected_category = st.sidebar.selectbox("🏷️ Select Category", categories)
else:
    selected_category = "All Categories"

# Hour range filter
if 'hour' in df.columns:
    hour_range = st.sidebar.slider(
        "⏰ Hour Range (24-hour format)",
        min_value=0,
        max_value=23,
        value=(6, 22),
        step=1
    )
else:
    hour_range = (0, 23)

# Apply filters
filtered_df = df.copy()

if selected_store != "All Stores" and 'store_location' in df.columns:
    filtered_df = filtered_df[filtered_df["store_location"] == selected_store]

if selected_category != "All Categories" and 'product_category' in df.columns:
    filtered_df = filtered_df[filtered_df["product_category"] == selected_category]

if 'hour' in df.columns:
    filtered_df = filtered_df[(filtered_df['hour'] >= hour_range[0]) & (filtered_df['hour'] <= hour_range[1])]

st.sidebar.info(f"📊 Showing {len(filtered_df):,} transactions")

st.divider()

# --- SECTION 1: STORE & CATEGORY BREAKDOWN ---
if 'store_location' in df.columns or 'product_category' in df.columns:
    st.subheader("📊 Revenue Analysis")
    
    col_left, col_right = st.columns(2)
    
    if 'store_location' in df.columns and 'revenue' in df.columns:
        with col_left:
            st.markdown("#### Revenue by Store")
            store_rev = filtered_df.groupby("store_location")["revenue"].sum().sort_values(ascending=False).reset_index()
            
            if len(store_rev) > 0:
                fig1 = px.bar(
                    store_rev,
                    x="store_location",
                    y="revenue",
                    color="revenue",
                    color_continuous_scale="Blues",
                    labels={"store_location": "Store", "revenue": "Revenue ($)"},
                    text="revenue"
                )
                fig1.update_traces(texttemplate='$%{text:,.0f}', textposition='auto')
                fig1.update_layout(showlegend=False, margin=dict(t=10, b=50))
                st.plotly_chart(fig1, use_container_width=True)
    
    if 'product_category' in df.columns and 'revenue' in df.columns:
        with col_right:
            st.markdown("#### Revenue by Category")
            cat_rev = filtered_df.groupby("product_category")["revenue"].sum().reset_index()
            
            if len(cat_rev) > 0:
                fig2 = px.pie(
                    cat_rev,
                    names="product_category",
                    values="revenue",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig2.update_layout(margin=dict(t=10))
                st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()

# --- SECTION 2: HOURLY TREND & TOP PRODUCTS ---
if 'hour' in df.columns or 'product_detail' in df.columns:
    st.subheader("⏰ Time & Product Analysis")
    
    col_left2, col_right2 = st.columns(2)
    
    if 'hour' in df.columns and 'revenue' in df.columns:
        with col_left2:
            st.markdown("#### Revenue by Hour of Day")
            hourly = filtered_df.groupby("hour")["revenue"].sum().reset_index().sort_values('hour')
            
            if len(hourly) > 0:
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=hourly['hour'],
                    y=hourly['revenue'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color='#8B4513', width=3),
                    marker=dict(size=8),
                    fill='tozeroy'
                ))
                fig3.update_layout(
                    title='',
                    xaxis_title='Hour (24h format)',
                    yaxis_title='Revenue ($)',
                    margin=dict(t=10, b=50),
                    hovermode='x unified'
                )
                st.plotly_chart(fig3, use_container_width=True)
    
    if 'product_detail' in df.columns and 'revenue' in df.columns:
        with col_right2:
            st.markdown("#### Top 10 Products by Revenue")
            top_products = (
                filtered_df.groupby("product_detail")["revenue"]
                .sum()
                .sort_values(ascending=True)
                .tail(10)
                .reset_index()
            )
            
            if len(top_products) > 0:
                fig4 = px.bar(
                    top_products,
                    x="revenue",
                    y="product_detail",
                    orientation="h",
                    color="revenue",
                    color_continuous_scale="Viridis",
                    labels={"product_detail": "Product", "revenue": "Revenue ($)"},
                    text="revenue"
                )
                fig4.update_traces(texttemplate='$%{text:,.0f}', textposition='auto')
                fig4.update_layout(margin=dict(t=10, b=50, l=200), showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)
    
    st.divider()

# --- SECTION 3: TRANSACTIONS ---
if 'hour' in df.columns:
    st.subheader("📅 Transaction Analysis")
    
    col_trans1, col_trans2 = st.columns(2)
    
    with col_trans1:
        st.markdown("#### Transaction Count by Hour")
        hourly_count = filtered_df.groupby("hour").size().reset_index(name='count').sort_values('hour')
        
        if len(hourly_count) > 0:
            fig5 = px.bar(
                hourly_count,
                x='hour',
                y='count',
                color='count',
                color_continuous_scale='Reds',
                labels={'hour': 'Hour (24h)', 'count': 'Number of Transactions'}
            )
            fig5.update_layout(margin=dict(t=10, b=50), showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
    
    if 'product_category' in df.columns and 'revenue' in df.columns:
        with col_trans2:
            st.markdown("#### Average Order Value by Category")
            avg_by_cat = filtered_df.groupby('product_category')['revenue'].mean().reset_index()
            
            if len(avg_by_cat) > 0:
                fig6 = px.bar(
                    avg_by_cat.sort_values('revenue', ascending=False),
                    x='product_category',
                    y='revenue',
                    color='revenue',
                    color_continuous_scale='Greens',
                    labels={'product_category': 'Category', 'revenue': 'Avg Order Value ($)'},
                    text='revenue'
                )
                fig6.update_traces(texttemplate='$%{text:,.2f}', textposition='auto')
                fig6.update_layout(margin=dict(t=10, b=50), showlegend=False)
                st.plotly_chart(fig6, use_container_width=True)
    
    st.divider()

# --- DATA TABLE ---
st.subheader("📋 Raw Data")

with st.expander("View Filtered Transaction Data", expanded=False):
    st.dataframe(
        filtered_df.head(100),
        use_container_width=True,
        height=400
    )

# --- FOOTER ---
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.metric("Total Filtered Revenue", f"${filtered_df['revenue'].sum():,.0f}" if 'revenue' in filtered_df.columns else "N/A")

with col_footer2:
    st.metric("Total Filtered Transactions", len(filtered_df))

with col_footer3:
    st.metric("Average Transaction Value", f"${filtered_df['revenue'].mean():.2f}" if 'revenue' in filtered_df.columns else "N/A")

st.caption("💡 Tip: Use sidebar filters to explore different segments of your data")
st.caption("📊 Afficionado Coffee Roasters | Data source: GitHub Repository | Powered by Streamlit")
