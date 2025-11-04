import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from streamlit_elements import elements, mui

# Page configuration
st.set_page_config(page_title="UF Sales Dashboard", layout="wide")

# Sidebar content
with st.sidebar:
    st.title("📊 Dashboard Info")
    st.markdown("---")
    st.info("Navigate between pages using the sidebar menu above")

# Dashboard title
st.title("UF - Sales Dashboard - v.3.1 (QA)")

# Create 4 columns for the filters
col1, col2, col3, col4 = st.columns(4)

# Column 1: Date Range
with col1:
    st.subheader("Date Range")
    date_options = [
        "Today",
        "Yesterday", 
        "Past 7 days",
        "Past 14 days",
        "Past 30 days",
        "Past 90 days",
        "Custom Range"
    ]
    selected_dates = st.multiselect(
        "Select Date Range:",
        date_options,
        default=["Today"]
    )

# Column 2: Customer Category
with col2:
    st.subheader("Customer Category")
    customer_categories = [
        "Select All",
        "Retail",
        "Trade",
        "Warehouse",
        "Distributor",
        "Online",
        "B2B",
        "B2C"
    ]
    selected_customers = st.multiselect(
        "Select Customer Categories:",
        customer_categories,
        default=["Select All"]
    )

# Column 3: Warehouse Options
with col3:
    st.subheader("Warehouse")
    warehouse_options = [
        "Select All",
        "Main Warehouse",
        "North Warehouse", 
        "South Warehouse",
        "East Warehouse",
        "West Warehouse",
        "Central Hub",
        "Distribution Center A",
        "Distribution Center B"
    ]
    selected_warehouses = st.multiselect(
        "Select Warehouses:",
        warehouse_options,
        default=["Select All"]
    )

# Column 4: Product Category
with col4:
    st.subheader("Product Category")
    product_categories = [
        "Select All",
        "Electronics",
        "Food & Beverages",
        "Clothing & Apparel",
        "Home & Garden",
        "Sports & Outdoors",
        "Books & Media",
        "Health & Beauty",
        "Automotive",
        "Toys & Games"
    ]
    selected_products = st.multiselect(
        "Select Product Categories:",
        product_categories,
        default=["Select All"]
    )

# Key Performance Metrics
st.markdown("---")
st.subheader("Key Performance Metrics")

# Create 6 columns for all metrics in one row
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5, metric_col6 = st.columns(6)

metrics_data = [
    ("Total Sales", "496.3k", "5.2%"),
    ("Avg Sales Per Customer", "497.8", "2.1%"),
    ("Avg Sales Per Order", "424.78", "1.8%"),
    ("Orders", "2,127", "8.3%"),
    ("Bottles Sold", "20,007", "12.5%"),
    ("Customers", "997", "6.7%")
]

columns = [metric_col1, metric_col2, metric_col3, metric_col4, metric_col5, metric_col6]

for col, (title, value, delta) in zip(columns, metrics_data):
    with col:
        with elements(f"metric_{title}"):
            mui.Card(
                mui.CardContent(
                    mui.Typography(title, variant="body2", color="textSecondary"),
                    mui.Typography(value, variant="h5", component="div"),
                    mui.Typography(delta, variant="body2", color="success.main" if delta.startswith("+") or not delta.startswith("-") else "error.main")
                ),
                sx={"minWidth": 120, "margin": 1}
            )

# --- CHARTS ---
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

# Pie Chart: Sales by Customer Category (LEFT SIDE)
with chart_col1:
    st.subheader("Sales - Customer Category")
    
    # Data for the pie chart
    pie_labels = ['Trade', 'Retail', 'Other']
    pie_values = [62.14, 36.00, 1.86]
    total_sales_value = "496.3k" # From the metric card

    pie_fig = go.Figure(data=[go.Pie(
        labels=pie_labels, 
        values=pie_values, 
        hole=.5, # Creates the donut chart effect
        textinfo='percent+label',
        marker_colors=['#FFA500', '#808080', '#FFD700']  # Orange, Grey, Yellow
    )])

    pie_fig.update_layout(
        annotations=[dict(
            text=f"Total<br>{total_sales_value}", 
            x=0.5, 
            y=0.5, 
            font_size=20, 
            showarrow=False
        )],
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(pie_fig, use_container_width=True)

# Bar Chart: Sales vs Month by Customer Category (RIGHT SIDE)
with chart_col2:
    st.subheader("Sales vs Month by Customer Category")
    
    # Sample data for the bar chart using st.bar_chart
    chart_data = pd.DataFrame({
        'Retail': [200, 210, 250, 280, 300, 320],
        'Trade': [350, 380, 400, 410, 430, 450],
        'Uncategorized': [50, 40, 60, 55, 70, 65],
        '(empty)': [20, 25, 30, 28, 35, 32]
    }, index=['January', 'February', 'March', 'April', 'May', 'June'])
    
    st.bar_chart(chart_data, height=350, use_container_width=False, width=500)

# Second Row of Charts
st.markdown("---")
chart_col3, chart_col4 = st.columns(2)

# Pie Chart: Sales by Product Category (LEFT SIDE)
with chart_col3:
    st.subheader("Sales - Product Category")
    
    # Data for the pie chart
    product_pie_labels = ['Uncategorized', 'Liquor & Spirits', 'Wine', 'Service', 'Beer', 'Other']
    product_pie_values = [54.82, 13.51, 11.38, 8.33, 3.93, 8.05]
    total_product_sales = "646,964.3"

    product_pie_fig = go.Figure(data=[go.Pie(
        labels=product_pie_labels, 
        values=product_pie_values, 
        hole=.5,
        textinfo='percent+label',
        marker_colors=['#00008B', '#4169E1', '#90EE90', '#006400', '#800080', '#808080']  # Dark Blue, Light Blue, Light Green, Dark Green, Purple, Grey
    )])

    product_pie_fig.update_layout(
        annotations=[dict(
            text=f"{total_product_sales}<br>TOTAL", 
            x=0.5, 
            y=0.5, 
            font_size=18, 
            showarrow=False
        )],
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(product_pie_fig, use_container_width=True)

# Table: Sales by Product Category (RIGHT SIDE)
with chart_col4:
    st.subheader("Sales - Product Category Details")
    
    # Data for the table
    product_table_data = {
        'Product Category': [
            'Uncategorized',
            'Liquor & Spirits',
            'Wine',
            'Service',
            'Beer',
            'Low Alcohol & Alcohol-Free Beverages',
            'POSM',
            'Tea',
            'Cordials, Syrups & Squash',
            'Non-Alcoholic',
            'Other Categories (3 more)'
        ],
        'Sales': [
            356755.57,
            87399.90,
            73598.88,
            53879.59,
            25395.73,
            11178.16,
            10463.14,
            9737.65,
            6687.34,
            6422.49,
            0.00
        ],
        'Count': [
            1486,
            348,
            237,
            53,
            49,
            9,
            30,
            50,
            48,
            24,
            0
        ]
    }
    
    product_df = pd.DataFrame(product_table_data)
    
    # Format the sales column with comma separator
    product_df['Sales'] = product_df['Sales'].apply(lambda x: f"{x:,.2f}" if x > 0 else "-")
    product_df['Count'] = product_df['Count'].apply(lambda x: str(x) if x > 0 else "-")
    
    st.dataframe(product_df, use_container_width=True, height=400)
    st.caption("Total: 13 rows")

# Third Row of Charts - Line Graphs
st.markdown("---")
chart_col5, chart_col6 = st.columns(2)

# Line Chart 1: Sales - Order View (LEFT SIDE)
with chart_col5:
    st.subheader("Sales - Order View")
    
    # Data for the line chart
    months_order = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', 
                    '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
                    '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                    '2025-07', '2025-08', '2025-09']
    
    orders_count = [94, 67, 58, 90, 96, 77, 107, 122, 109, 117, 100, 130, 150, 121, 92, 85, 78, 95, 110, 88, 75]
    avg_order_value = [420, 445, 410, 465, 480, 455, 490, 510, 495, 505, 485, 520, 540, 515, 475, 460, 450, 470, 495, 465, 440]
    
    order_fig = go.Figure()
    
    order_fig.add_trace(go.Scatter(
        x=months_order,
        y=orders_count,
        mode='lines',
        name='# of Orders',
        line=dict(color='#00FF00', width=3),  # Green color
        yaxis='y'
    ))
    
    order_fig.add_trace(go.Scatter(
        x=months_order,
        y=avg_order_value,
        mode='lines',
        name='Average Order Value',
        line=dict(color='#32CD32', width=3, dash='dash'),  # Light green color
        yaxis='y2'
    ))
    
    order_fig.update_layout(
        xaxis=dict(title="Month", tickangle=-45),
        yaxis=dict(
            title="# of Orders",
            side='left',
            range=[0, 160]
        ),
        yaxis2=dict(
            title="Average Order Value",
            overlaying='y',
            side='right'
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=60, b=80),
        hovermode='x unified'
    )
    
    st.plotly_chart(order_fig, use_container_width=True)

# Line Chart 2: Sales - Customer View (RIGHT SIDE)
with chart_col6:
    st.subheader("Sales - Customer View")
    
    # Data for the line chart
    customers_count = [75, 55, 48, 72, 78, 65, 88, 98, 90, 95, 82, 105, 120, 98, 75, 68, 62, 78, 90, 72, 60]
    avg_sales_per_customer = [520, 540, 510, 570, 590, 565, 600, 620, 605, 615, 595, 630, 650, 625, 585, 570, 560, 580, 605, 575, 550]
    
    customer_fig = go.Figure()
    
    customer_fig.add_trace(go.Scatter(
        x=months_order,
        y=customers_count,
        mode='lines',
        name='Customers',
        line=dict(color='#00FF00', width=3),  # Green color
        yaxis='y'
    ))
    
    customer_fig.add_trace(go.Scatter(
        x=months_order,
        y=avg_sales_per_customer,
        mode='lines',
        name='Average Sales Per Customer',
        line=dict(color='#32CD32', width=3, dash='dash'),  # Light green color
        yaxis='y2'
    ))
    
    customer_fig.update_layout(
        xaxis=dict(title="Month", tickangle=-45),
        yaxis=dict(
            title="Customers",
            side='left',
            range=[0, 130]
        ),
        yaxis2=dict(
            title="Average Sales Per Customer",
            overlaying='y',
            side='right'
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=60, b=80),
        hovermode='x unified'
    )
    
    st.plotly_chart(customer_fig, use_container_width=True)

# Fourth Row - Product Category Sales Over Time
st.markdown("---")
st.subheader("Sales by Product Category Over Time")

# Data for the bar chart
months_product = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', 
                  '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
                  '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                  '2025-07', '2025-08', '2025-09']

# Sample sales data for each product category
product_bar_data = pd.DataFrame({
    'Beer': [2500, 2300, 2100, 2600, 2700, 2400, 2800, 2900, 2750, 2850, 2650, 3000, 3100, 2950, 2600, 2400, 2300, 2500, 2700, 2600, 2400],
    'Liquor & Spirits': [8500, 8000, 7500, 9000, 9200, 8600, 9500, 9800, 9400, 9600, 9000, 10000, 10500, 10000, 9000, 8500, 8000, 8700, 9300, 8900, 8500],
    'Uncategorized': [35000, 32000, 30000, 38000, 40000, 36000, 42000, 45000, 43000, 44000, 41000, 48000, 50000, 47000, 40000, 38000, 36000, 39000, 42000, 40000, 38000],
    'Non-Alcoholic': [600, 580, 550, 640, 660, 610, 680, 700, 670, 690, 640, 720, 750, 710, 620, 590, 560, 610, 650, 630, 590],
    'Wine': [7000, 6500, 6000, 7200, 7400, 6900, 7600, 7800, 7500, 7700, 7200, 8000, 8300, 7900, 7000, 6700, 6400, 6900, 7400, 7100, 6700],
    'Accessories': [1200, 1100, 1000, 1250, 1300, 1200, 1350, 1400, 1330, 1380, 1280, 1450, 1500, 1430, 1250, 1180, 1120, 1220, 1320, 1260, 1180],
    'Service': [5200, 4900, 4600, 5500, 5700, 5300, 5900, 6100, 5800, 6000, 5600, 6400, 6600, 6300, 5500, 5200, 5000, 5400, 5800, 5600, 5200],
    'POSM': [1000, 950, 900, 1100, 1150, 1050, 1200, 1250, 1180, 1220, 1130, 1300, 1350, 1280, 1100, 1040, 980, 1070, 1160, 1110, 1040],
    'Tea': [950, 900, 850, 1050, 1100, 1000, 1150, 1200, 1130, 1170, 1080, 1250, 1300, 1230, 1050, 990, 940, 1020, 1120, 1070, 990],
    'Supplement': [800, 750, 700, 850, 900, 820, 920, 950, 900, 930, 860, 1000, 1050, 990, 850, 800, 760, 830, 900, 860, 800],
    'Cordials, Syrups & Squash': [650, 610, 580, 680, 710, 650, 730, 760, 720, 745, 690, 800, 830, 785, 680, 640, 610, 660, 720, 685, 640],
    'Barware': [550, 520, 490, 580, 610, 560, 630, 660, 620, 645, 595, 700, 730, 690, 580, 550, 520, 565, 620, 590, 550],
    'Low Alcohol': [1100, 1050, 980, 1180, 1230, 1130, 1280, 1330, 1260, 1300, 1200, 1400, 1450, 1370, 1180, 1120, 1060, 1150, 1250, 1190, 1120]
}, index=months_product)

st.bar_chart(product_bar_data, height=500)

# Footer
st.markdown("---")
st.markdown("*UF Sales Dashboard v.3.1 (QA) - Quality Assurance Environment*")