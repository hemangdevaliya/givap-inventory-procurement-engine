import os
import io
import streamlit as pd_web_app
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# 1. Load Secure Environment Variables from .env File Matrix
load_dotenv()

# 2. Page Configuration for Commercial Application
pd_web_app.set_page_config(
    page_title="GIVAP - Secure Postgres Enterprise Engine",
    page_icon="🛒",
    layout="wide"
)

# 3. Environment-Backed Secure Database Connection Factory
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "my_retail_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432")
    )

# 4. Pull Live State directly from PostgreSQL Engine Core
def fetch_live_inventory():
    conn = get_db_connection()
    query = """
        SELECT 
            sku AS "SKU", 
            item_name AS "Item_Name", 
            weekly_units_sold AS "Weekly_Units_Sold", 
            current_stock AS "Current_Stock", 
            unit_cost_inr AS "Unit_Cost_INR", 
            selling_price_inr AS "Selling_Price_INR"
        FROM inventory_ledger
        ORDER BY item_name ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 5. Dynamic Real-Time Analytical Decision Rules Engine
def compute_procurement_analytics(df):
    working_df = df.copy()
    working_df['Profit_Per_Unit'] = working_df['Selling_Price_INR'] - working_df['Unit_Cost_INR']
    working_df['Total_Profit'] = working_df['Weekly_Units_Sold'] * working_df['Profit_Per_Unit']
    
    def evaluate_stock_action(row):
        sold = row['Weekly_Units_Sold']
        stock = row['Current_Stock']
        profit = row['Profit_Per_Unit']
        
        HIGH_SALES_LIMIT = 300
        LOW_SALES_LIMIT = 5
        HIGH_PROFIT_LIMIT = 20
        
        if sold >= HIGH_SALES_LIMIT and stock < (sold * 0.5):
            return "add stock"
        elif sold <= LOW_SALES_LIMIT and stock > (sold * 10):
            return "remove stock"
        elif (sold * 0.8) <= stock <= (sold * 1.5):
            return "no new stock needed"
        elif sold > LOW_SALES_LIMIT and stock > (sold * 2):
            if profit >= HIGH_PROFIT_LIMIT:
                return "change stock"
            else:
                return "remove stock"
        return "no new stock needed"

    working_df['Decision_Result'] = working_df.apply(evaluate_stock_action, axis=1)
    return working_df

# 6. Interface Header Layout
pd_web_app.title("🛒 GIVAP: PostgreSQL Automated Procurement Engine")
pd_web_app.markdown("---")

# Verify connection variables are loaded before trying to fetch
try:
    live_data_df = fetch_live_inventory()
except Exception as conn_error:
    pd_web_app.error("🚨 Database Connection Error! Verify that your `.env` credentials match your running PostgreSQL instance configuration values.")
    pd_web_app.stop()

# 7. Live Operations Terminal Panel (SQL Mutation Updates)
pd_web_app.header("⚡ Live Register Terminal")
col_register_1, col_register_2 = pd_web_app.columns(2)

with col_register_1:
    pd_web_app.subheader("💸 Record Customer Checkout Sale")
    selected_sell_item = pd_web_app.selectbox("Select Item Sold", live_data_df['Item_Name'].unique(), key="sell_select")
    sell_quantity = pd_web_app.number_input("Units Purchased by Customer", min_value=1, value=1, step=1, key="sell_qty")
    
    if pd_web_app.button("Execute Transaction Invoice", type="primary"):
        row = live_data_df[live_data_df['Item_Name'] == selected_sell_item].iloc[0]
        current_available = row['Current_Stock']
        item_sku = row['SKU']
        
        if current_available >= sell_quantity:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventory_ledger 
                SET current_stock = current_stock - %s,
                    weekly_units_sold = weekly_units_sold + %s
                WHERE sku = %s;
            """, (sell_quantity, sell_quantity, item_sku))
            conn.commit()
            cursor.close()
            conn.close()
            
            pd_web_app.success(f"Invoice Success! Database decremented {sell_quantity} units of {selected_sell_item}.")
            live_data_df = fetch_live_inventory()
        else:
            pd_web_app.error(f"Stockout Alert! Cannot sell. Only {current_available} units left inside Postgres storage block.")

with col_register_2:
    pd_web_app.subheader("📦 Receive Inward Distributor Stock")
    selected_buy_item = pd_web_app.selectbox("Select Product to Inward", live_data_df['Item_Name'].unique(), key="buy_select")
    buy_quantity = pd_web_app.number_input("Units Supplied by Distributor", min_value=1, value=50, step=1, key="buy_qty")
    
    if pd_web_app.button("Log Inward Supply Shipment", type="secondary"):
        row = live_data_df[live_data_df['Item_Name'] == selected_buy_item].iloc[0]
        item_sku = row['SKU']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventory_ledger 
            SET current_stock = current_stock + %s
            WHERE sku = %s;
        """, (buy_quantity, item_sku))
        conn.commit()
        cursor.close()
        conn.close()
        
        pd_web_app.success(f"Stock Replenished! Added {buy_quantity} units to database ledger record.")
        live_data_df = fetch_live_inventory()

pd_web_app.markdown("---")

# 8. Real-Time Procurement Console and Ledger Panel
pd_web_app.header("📊 Real-Time Inventory Procurement Dashboard")

analyzed_df = compute_procurement_analytics(live_data_df)


# CALCULATE NET TOTAL PROFIT: Summing the Total_Profit column metrics
net_total_profit = analyzed_df['Total_Profit'].sum()

# Display Net Total Profit as a high-impact financial card indicator
col_metric, _ = pd_web_app.columns([1, 3])
with col_metric:
    pd_web_app.metric(
        label="💰 Weekly Net Total Profit", 
        value=f"₹{net_total_profit:,.2f}",
        help="The aggregated total weekly profit yield generated across all active inventory movements."
    )
    

def style_decision_cells(val):
    if val == "add stock":
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif val == "remove stock":
        return 'background-color: #e2e3e5; color: #383d41; font-weight: bold;'
    elif val == "change stock":
        return 'background-color: #fff3cd; color: #856404; font-weight: bold;'
    return 'background-color: #d4edda; color: #155724;'

styled_table = analyzed_df.style.map(style_decision_cells, subset=['Decision_Result']).format({
    'Unit_Cost_INR': '₹{:.2f}',
    'Selling_Price_INR': '₹{:.2f}',
    'Profit_Per_Unit': '₹{:.2f}',
    'Total_Profit': '₹{:.2f}'
})

pd_web_app.dataframe(styled_table, use_container_width=True)

# 9. One-Click Instant Data Export Operation
pd_web_app.markdown("### 📥 Extract Operational Data Reports")

csv_buffer = io.StringIO()
analyzed_df.to_csv(csv_buffer, index=False)
csv_string_payload = csv_buffer.getvalue()

pd_web_app.download_button(
    label="Export Decision Sheet (CSV)",
    data=csv_string_payload,
    file_name="postgres_procurement_result.csv",
    mime="text/csv",
    use_container_width=False,
    type="primary",

)
