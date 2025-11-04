import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
import numpy as np

# -----------------
# 1. PAGE CONFIG
# -----------------
# Set the page to wide layout
st.set_page_config(layout="wide")

# -----------------
# 2. LOTTIE ANIMATION (As requested)
# -----------------
# Function to load Lottie animation from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animation URL (a "data" animation)
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_zlrpnoxz.json"
lottie_json = load_lottieurl(lottie_url)


# -----------------
# 3. SAMPLE DATA (Based on screenshots)
# -----------------
# We'll create Pandas DataFrames that mimic the data in your charts.

# Data for the small chart in the first KPI card
kpi_chart_data = pd.DataFrame(
    np.random.rand(10, 1),
    columns=['data']
)

# Data for "Sales - Customer Segment" (Stacked Bar)
df_sales_segment = pd.DataFrame({
    'month': ['Jan 2025', 'Jan 2025', 'Apr 2025', 'Apr 2025', 'Jul 2025', 'Jul 2025', 'Oct 2025', 'Oct 2025'],
    'segment': ['Retail', 'Trade', 'Retail', 'Trade', 'Retail', 'Trade', 'Retail', 'Trade'],
    'sales_sgd': [50, 25, 200, 100, 255, 150, 220, 80]
})

# Data for "Depletion - Product" (Simple Bar)
df_depletion_product = pd.DataFrame({
    'Item': ['Loca Loka Blanca', 'Loca Loka Reposado'],
    'Quantity': [753, 226]
})

# Data for "Top Customers" (Horizontal Bar)
df_top_customers = pd.DataFrame({
    'customer': [
        'Pullman Singapore Hill Street (El Chido)', 'Commonwealth Concepts Pte Ltd (Kinki)',
        'Ironhill Hospitality Pte Ltd', 'Ipanema World Music Bar', 'Marina Bay Sands Pte. Ltd.',
        'Redhill Communications', "Morton's of Chicago The Steakhouse", 'Lavi Tapas',
        'Chimichanga Little India', 'Pocket Rocket', '3 Delinquents',
        'Commonwealth Concepts Pte Ltd (Ginkgo by Kinki)', 'Other'
    ],
    'Quantity': [130, 124, 116, 70, 53, 36, 35, 27, 26, 25, 22, 21, 255]
}).sort_values(by='Quantity', ascending=True) # Sort for horizontal bar chart

# Data for "Depletion by SKU" (Donut Chart)
df_depletion_sku = pd.DataFrame({
    'SKU': ['Loca Loka Blanca', 'Loca Loka Reposado'],
    'Value': [76, 24] # These are percentages from the chart
})

# Data for "Monthly Depletion Categorisation" (Table)
df_monthly_depletion = pd.DataFrame({
    'Monthly Depletion': ['1', '2', '3', '4', '>24', '6', '7-12', '13-18'],
    '# of Customer': [13, 8, 4, 1, 26, 1, 1, 3],
    'Customer Names': [
        "21 Carpenter - Kee's, Bar Bon Funk, Bar Madame, Brooklyn Bar, Burnt Ends...",
        "3 Delinquents , 67 Pall Mall Singapore Ltd, Andaz Hotel (Mr Stork), Artemis Grill & Sky Bar...",
        "Chimichanga Little India, Lavi Tapas, Morton's of Chicago The Steakhouse, Pocket Rocket",
        "Redhill Communications",
        "Capella Hotel, Chimi's 313 Somerset, Chimichanga Holland Village...",
        "Marina Bay Sands Pte. Ltd.",
        "Ipanema World Music Bar",
        "Commonwealth Concepts Pte Ltd (Kinki), Ironhill Hospitality Pte Ltd, Pullman Singapore Hill Street (El Chido)"
    ]
})

# Data for "Urbanfindr Monthly Sales" (Table)
df_monthly_sales = pd.DataFrame({
    'Customer_Name': [
        'Ironhill Hospitality Pte Ltd', 'Pullman Singapore Hill Street (El Chido)',
        'Commonwealth Concepts Pte Ltd (Kinki)', 'Marina Bay Sands Pte. Ltd.',
        'Lavi Tapas', '67 Pall Mall Singapore Ltd', 'Artemis Grill & Sky Bar',
        "21 Carpenter - Kee's", '3 Delinquents'
    ],
    'January': [11, 0, 1, 0, 0, 0, 0, 0, 0],
    'February': [4, 2, 2, 0, 0, 0, 0, 0, 4],
    'March': [8, 2, 3, 0, 0, 0, 0, 0, 0],
    'April': [2, 1, 1, 0, 0, 1, 1, 2, 2],
    'May': [6, 4, 5, 0, 4, 0, 1, 2, 0],
    'June': [4, 0, 2, 1, 3, 0, 1, 0, 0],
    'July': [5, 2, 0, 5, 0, 0, 0, 0, 0],
    'August': [0, 2, 0, 3, 0, 2, 0, 0, 0],
    'September': [0, 1, 0, 0, 0, 1, 0, 0, 0]
})

# -----------------
# 4. DASHBOARD LAYOUT
# -----------------

# --- Row 1: Filters ---
f1, f2, f3, f4, f5 = st.columns(5)
with f1:
    st.date_input("Date", (pd.to_datetime('2025-01-01'), pd.to_datetime('2025-10-31')))
with f2:
    st.selectbox("Status", ["All", "Pending", "Completed"])
with f3:
    st.selectbox("Item", ["All", "Loca Loka Blanca", "Loca Loka Reposado"])
with f4:
    st.selectbox("Customer Category", ["All", "Retail", "Trade"])
with f5:
    st.selectbox("Ironhill Toggle", ["All", "Yes", "No"])

st.divider()

# --- Row 2: Title & Lottie ---
t1, t2 = st.columns([4, 1]) # Give 4/5 of the space to title, 1/5 to Lottie
with t1:
    st.title("Loca Loka Sales in Singapore 🥑")
    st.caption("This dashboard refreshes every minute")
with t2:
    st_lottie(lottie_json, height=120, key="data_animation")

# --- Row 3: KPI Metrics ---
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    # We add a small line chart *above* the metric, just like in the screenshot
    st.line_chart(kpi_chart_data, use_container_width=True, height=100)
    st.metric(label="No of Orders", value="166")

with kpi2:
    # A blank space to align the metrics (since the first one has a chart)
    st.empty() 
    st.metric(label="No of Customers", value="57")

with kpi3:
    st.empty()
    st.metric(label="Churned Customers", value="45")

with kpi4:
    st.empty()
    st.metric(label="Repeat Buyers", value="24")

with kpi5:
    st.empty()
    st.metric(label="Buyer Rate", value="41.38")

st.divider()

# --- Row 4: Charts (Sales Segment & Depletion) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sales - Customer Segment")
    # Create a stacked bar chart with Plotly Express
    fig_stacked_bar = px.bar(
        df_sales_segment, 
        x='month', 
        y='sales_sgd', 
        color='segment',
        title="",
        labels={'sales_sgd': 'Sales (SGD)', 'month': 'Month', 'segment': 'Segment'},
        color_discrete_map={'Retail': '#9d84c0', 'Trade': '#cac0db'}
    )
    # Update layout to match screenshot
    fig_stacked_bar.update_layout(
        barmode='stack',
        xaxis_title=None,
        yaxis_title="loca loka, sgd",
        legend_title=None,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_stacked_bar, use_container_width=True)

with c2:
    st.subheader("Depletion - Product")
    # Create a simple bar chart
    fig_simple_bar = px.bar(
        df_depletion_product,
        x='Item',
        y='Quantity',
        color='Item', # Color by item
        text='Quantity', # Add text labels
        color_discrete_map={'Loca Loka Blanca': '#836ab5', 'Loca Loka Reposado': '#a898cf'}
    )
    # Update layout
    fig_simple_bar.update_layout(
        xaxis_title="Item",
        yaxis_title="Quantity",
        showlegend=False # Hide legend as colors are clear
    )
    fig_simple_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_simple_bar, use_container_width=True)


# --- Row 5: Charts (Top Customers & SKU Depletion) ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("Top Customers")
    # Create a horizontal bar chart
    fig_horiz_bar = px.bar(
        df_top_customers,
        x='Quantity',
        y='customer',
        orientation='h', # This makes it horizontal
        text='Quantity',
        color_discrete_sequence=['#836ab5'] * len(df_top_customers) # Single color
    )
    # Update layout to match
    fig_horiz_bar.update_layout(
        xaxis_title="Quantity",
        yaxis_title="Customer",
        yaxis=dict(title=None), # Hide y-axis label
        xaxis=dict(title=None)  # Hide x-axis label
    )
    fig_horiz_bar.update_traces(textposition='auto')
    st.plotly_chart(fig_horiz_bar, use_container_width=True)

with c4:
    st.subheader("Depletion by SKU")
    # Create a donut chart using Plotly Graph Objects (go)
    fig_donut = go.Figure(data=[go.Pie(
        labels=df_depletion_sku['SKU'], 
        values=df_depletion_sku['Value'], 
        hole=.6, # This creates the donut hole
        marker_colors=['#836ab5', '#f0eef5'],
        textinfo='percent',
        insidetextorientation='radial'
    )])
    
    # Add the text in the middle
    fig_donut.update_layout(
        annotations=[dict(
            text="933<br>TOTAL", 
            x=0.5, y=0.5, 
            font_size=20, 
            showarrow=False
        )],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# --- Row 6: Tables (Depletion & Monthly Sales) ---
st.subheader("Monthly Depletion Categorisation")
st.dataframe(df_monthly_depletion, use_container_width=True)

st.subheader("Urbanfindr Monthly Sales")
st.dataframe(df_monthly_sales, use_container_width=True)