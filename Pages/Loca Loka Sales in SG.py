import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from streamlit_lottie import st_lottie

# -----------------
# 1. PAGE CONFIG & LOTTIE
# -----------------
st.set_page_config(layout="wide")

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animation URL
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_zlrpnoxz.json"
lottie_json = load_lottieurl(lottie_url)

# -----------------
# 2. SAMPLE DATA CREATION (for all tabs)
# -----------------

# --- Data for "Overview" Tab ---

# Data for Chart 1 & 5 & 6 (Stacked Bars)
months = ['2024-12', '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09']
# We create "melted" dataframes, which is the format Plotly loves
df_primary_depletion = pd.DataFrame({
    'month': months * 2,
    'SKU': ['Loca Loka Blanco']*10 + ['Loca Loka Reposado']*10,
    'total_quantity': [50, 80, 70, 90, 150, 120, 110, 60, 100, 100] + [30, 40, 30, 40, 60, 50, 80, 50, 50, 40]
})

df_secondary_depletion = pd.DataFrame({
    'month': months * 3,
    'Segment': ['Ironhill']*10 + ['UrbanFindr']*10 + ['Platinum']*10,
    'total_quantity': [30, 40, 50, 60, 70, 80, 90, 100, 80, 60] + [40, 50, 30, 60, 120, 110, 80, 90, 70, 50] + [20, 30, 20, 40, 30, 20, 10, 15, 20, 10]
})

df_platinum_loca_loka = pd.DataFrame({
    'month': months * 2,
    'SKU': ['Loca Loka Blanco']*10 + ['Loca Loka Reposado']*10,
    'total_quantity': [5, 8, 7, 9, 15, 12, 11, 6, 10, 10] + [3, 4, 3, 4, 6, 5, 8, 5, 5, 4]
})

df_urbanfindr_loca_loka = pd.DataFrame({
    'month': months * 2,
    'SKU': ['Loca Loka Blanco']*10 + ['Loca Loka Reposado']*10,
    'total_quantity': [25, 30, 20, 40, 100, 90, 70, 80, 60, 40] + [10, 20, 10, 20, 30, 20, 40, 20, 20, 10]
})

# Data for Chart 3 & 4 (Bar + Line Combo)
combo_months = ['2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09']
df_platinum_sales_qty = pd.DataFrame({
    'month': combo_months,
    'total_quantity': [5, 10, 8, 18, 15, 75, 80],
    'unique_outlets': [2, 5, 4, 8, 20, 15, 100]
})

df_urbanfindr_sales_qty = pd.DataFrame({
    'month': ['2025-05', '2025-06', '2025-07', '2025-08', '2025-09', '2025-10'],
    'total_quantity': [10, 12, 8, 10, 15, 10],
    'unique_outlets': [100, 160, 50, 30, 60, 30]
})


# --- Data for "UrbanFindr Customers" Tab ---
df_active_buyers_urbanfindr = pd.DataFrame({
    'customer': ["21 Carpenter - Kee's", "3 Delinquents", "Ashwin Segar", "Bar Bon Funk", "Bar Madame", "Brooklyn Bar"],
    'last_purchase': ["May 3, 2025, 5:49 AM", "Apr 10, 2025, 5:27 AM", "Jan 20, 2025, 5:12 AM", "Feb 17, 2025, 6:45 AM", "Apr 29, 2025, 6:42 AM", "May 2, 2025, 10:41 AM"],
    'active_windows': [1, 2, 1, 1, 1, 1],
    'customer_category': ['Trade', 'Trade', 'Retail', 'Trade', 'Trade', 'Trade'],
    'buyer_status': ['Lapsed', 'Lapsed', 'Lapsed', 'Lapsed', 'Lapsed', 'Lapsed']
})

df_urbanfindr_orders_month = pd.DataFrame({
    'Customer_Name': ['Ironhill Hospitality Pte Ltd', 'Pullman Singapore Hill Street (El Chido)', 'Commonwealth Concepts Pte Ltd (Kinki)', 'Marina Bay Sands Pte. Ltd.', 'Ipanema World Music Bar', 'Lavi Tapas'],
    'January': [6, 1, 2, 0, 0, 0], 'February': [3, 1, 3, 0, 0, 0], 'March': [6, 2, 1, 0, 0, 0],
    'April': [1, 2, 4, 1, 0, 0], 'May': [2, 8, 4, 2, 3, 0], 'June': [4, 2, 2, 1, 2, 0],
    'July': [0, 1, 0, 5, 0, 0], 'August': [1, 0, 0, 3, 0, 0]
})

df_urbanfindr_bottles_month = pd.DataFrame({
    'Customer_Name': ['Pullman Singapore Hill Street (El Chido)', 'Commonwealth Concepts Pte Ltd (Kinki)', 'Ironhill Hospitality Pte Ltd', 'Ipanema World Music Bar', 'Redhill Communications', "Morton's of Chicago The Steakhouse"],
    'January_Bottles': [6, 19, 9, 0, 0, 0], 'February_Bottles': [12, 15, 19, 0, 0, 0], 'March_Bottles': [6, 12, 19, 0, 0, 0],
    'April_Bottles': [12, 27, 1, 26, 0, 0], 'May_Bottles': [40, 2, 23, 0, 0, 0], 'June_Bottles': [4, 2, 1, 4, 36, 0]
})

# --- Data for "Platinum Customers" Tab ---
df_active_buyers_platinum = pd.DataFrame({
    'customer': ['THE URBANFINDR PTE. LTD. - EXTRA SPACE BOON KENG WAREHOUSE', 'IRONHILL HOSPITALITY PTE. LTD.', 'ATHENA ALLIANCE PTE. LTD. - MEZAME', 'LEGENDS CULTURE LLP', 'WARREN GOLF & COUNTRY CLUB', 'IPG HOSPITALITY PTE. LTD. - AKASA'],
    'last_purchase': ['Sep 30, 2025', 'Jul 7, 2025', 'Sep 12, 2025', 'Sep 8, 2025', 'Jun 20, 2025', 'Jun 26, 2025'],
    'active_windows': [4, 4, 2, 2, 1, 1],
    'channel': ['WHOLESALER', 'WHOLESALER', 'ON', 'ON', 'ON', 'ON'],
    'buyer_status': ['Platinum Regular', 'Lapsed', 'High Value Occasional', 'Standard', 'Lapsed', 'Lapsed']
})

df_platinum_sales_bottles = pd.DataFrame({
    'Customer_Name': ['ATHENA ALLIANCE PTE. LTD. - MEZAME', 'CENTROFOOD INDUSTRIES PTE. LTD. - THE FAMOUS KITCHEN', 'BAR. TER HDGS PTE. LTD. - BAR. TER', 'CURIO CAT PTE. LTD. - SIDES', 'KIN F & B PTE. LTD. - YEN IZAKAYA', 'LEGENDS CULTURE LLP'],
    'January': [0, 0, 0, 0, 0, 0], 'February': [0, 0, 0, 0, 0, 0], 'March': [0, 0, 0, 0, 0, 0],
    'April': [0, 0, 0, 0, 0, 0], 'May': [0, 0, 0, 0, 0, 0], 'June': [1, 0, 0, 0, 0, 1],
    'July': [1, 0, 0, 0, 2, 0]
})

# --- Data for "Pullman Hill Street" Tab ---
df_pullman_sales = pd.DataFrame({
    'Customer_Name': ['Pullman Singapore Hill Street (El Chido)', 'EL Development (Ventures) Pte Ltd c/o Pullman Singapore Hill Street'],
    'January_Bottles': [None, None], 'February_Bottles': [6, 6], 'March_Bottles': [12, None],
    'April_Bottles': [26, 6], 'May_Bottles': [None, None]
})


# -----------------
# 3. DASHBOARD UI
# -----------------

# --- Title & Lottie ---
t1, t2 = st.columns([4, 1])
with t1:
    st.title("Loca Loka Sales in SG 🥑")
with t2:
    st_lottie(lottie_json, height=100, key="data_animation")

# --- Create Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview", 
    "UrbanFindr Customers", 
    "Platinum Customers", 
    "Pullman Hill Street"
])


# --- Populate Tab 1: Overview ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Primary Depletion (Bottle)")
        # Plotly Express stacked bar
        fig1 = px.bar(
            df_primary_depletion, x="month", y="total_quantity", color="SKU",
            title="",
            color_discrete_map={
                'Loca Loka Blanco': '#f08a69', 
                'Loca Loka Reposado': '#f7b9a5'
            }
        )
        fig1.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Platinum Sales by Qty & # of Outlets")
        # Plotly Graph Objects combo chart
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        # Add Bar
        fig3.add_trace(go.Bar(
            x=df_platinum_sales_qty['month'], y=df_platinum_sales_qty['total_quantity'],
            name='total_quantity', marker_color='#836ab5'
        ), secondary_y=False)
        # Add Line
        fig3.add_trace(go.Scatter(
            x=df_platinum_sales_qty['month'], y=df_platinum_sales_qty['unique_outlets'],
            name='unique_outlets', mode='lines+markers', line=dict(color='#a898cf')
        ), secondary_y=True)
        fig3.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig3.update_yaxes(title_text="total_quantity", secondary_y=False)
        fig3.update_yaxes(title_text="unique_outlets", secondary_y=True)
        st.plotly_chart(fig3, use_container_width=True)

        st.subheader("Platinum Loca Loka Sale (Bottle)")
        fig5 = px.bar(
            df_platinum_loca_loka, x="month", y="total_quantity", color="SKU",
            title="",
            color_discrete_map={
                'Loca Loka Blanco': '#f08a69', 
                'Loca Loka Reposado': '#f7b9a5'
            }
        )
        fig5.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.subheader("Secondary Depletion")
        fig2 = px.bar(
            df_secondary_depletion, x="month", y="total_quantity", color="Segment",
            title="",
            color_discrete_map={
                'Ironhill': '#55a630', 
                'UrbanFindr': '#aacc00', 
                'Platinum': '#d4d4d4'
            }
        )
        fig2.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("UrbanFindr sales by Qty & Outlet")
        # Plotly Graph Objects combo chart
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        # Add Bar
        fig4.add_trace(go.Bar(
            x=df_urbanfindr_sales_qty['month'], y=df_urbanfindr_sales_qty['total_quantity'],
            name='total_quantity', marker_color='#836ab5'
        ), secondary_y=False)
        # Add Line
        fig4.add_trace(go.Scatter(
            x=df_urbanfindr_sales_qty['month'], y=df_urbanfindr_sales_qty['unique_outlets'],
            name='unique_outlets', mode='lines+markers', line=dict(color='#70e000')
        ), secondary_y=True)
        fig4.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig4.update_yaxes(title_text="total_quantity", secondary_y=False)
        fig4.update_yaxes(title_text="unique_outlets", secondary_y=True)
        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("UrbanFindr Loca Loka Sale (Bottle)")
        fig6 = px.bar(
            df_urbanfindr_loca_loka, x="month", y="total_quantity", color="SKU",
            title="",
            color_discrete_map={
                'Loca Loka Blanco': '#f08a69', 
                'Loca Loka Reposado': '#f7b9a5'
            }
        )
        fig6.update_layout(legend_title=None, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig6, use_container_width=True)


# --- Populate Tab 2: UrbanFindr Customers ---
with tab2:
    st.subheader("Active Buyers")
    st.caption("Repeat Buyers - All Customer Categories for UrbanFindr")
    st.dataframe(df_active_buyers_urbanfindr, use_container_width=True)

    st.subheader("UrbanFindr Sales - # of Orders per Month")
    st.dataframe(df_urbanfindr_orders_month, use_container_width=True)

    st.subheader("UrbanFindr Sales - by Bottles")
    st.dataframe(df_urbanfindr_bottles_month, use_container_width=True)

# --- Populate Tab 3: Platinum Customers ---
with tab3:
    st.subheader("Active Buyers")
    st.caption("Repeat Buyers - All Customer Categories for UrbanFindr") # Kept caption as per screenshot
    st.dataframe(df_active_buyers_platinum, use_container_width=True)
    
    st.subheader("Platinum Monthly Sales (by Bottles)")
    st.dataframe(df_platinum_sales_bottles, use_container_width=True)

# --- Populate Tab 4: Pullman Hill Street ---
with tab4:
    st.subheader("Loca Loka Sales by Bottle (Pullman Hill St)")
    st.dataframe(df_pullman_sales, use_container_width=True)