import streamlit as st
import pymysql
import pandas as pd

# Connect to the database
mydb = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='G@n#31#P@s',
    database="retail_orders",
    autocommit=True
)
mycursor = mydb.cursor()

st.markdown(
    "<h1 style='text-align: center; font-size: 55px;'>RETAIL ORDERS</h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center;'>DATA INSIGHTS</h2>", 
    unsafe_allow_html=True
)

# Function to execute query and display results

def run_query(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in mycursor.description])
    st.table(df)

# Dropdown to select query type

query_options = {
    "1.  Top 10 highest revenue-generating products": '''
        SELECT t1.product_id, SUM(t1.sale_price * t1.quantity) AS revenue
        FROM table_0 t0
        JOIN table_1 t1 ON t0.order_id = t1.order_id
        GROUP BY t1.product_id
        ORDER BY revenue DESC
        LIMIT 10;
    ''',
    "2.  Top 5 cities with highest profit margins": '''
        SELECT table_0.city, SUM(table_1.profit) AS total_profit
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.city
        ORDER BY total_profit DESC
        LIMIT 5;
    ''',
    "3.  Calculate the total discount given for each category": '''
        SELECT table_0.category, SUM(table_1.discount) AS total_discount
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.category;
    ''',
    "4.  Average sale price per product category": '''
        SELECT table_0.category, AVG(table_1.sale_price) AS avg_sale_price
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.category;
    ''',
    "5.  Region with the highest average sale price": '''
        SELECT table_0.region, AVG(table_1.sale_price) AS avg_sale_price
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.region
        ORDER BY avg_sale_price DESC
        LIMIT 1;
    ''',
    "6.  Total profit per category": '''
        SELECT table_0.category, SUM(table_1.profit) AS total_profit
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.category;
    ''',
    "7.  Top 3 segments with the highest quantity of orders": '''
        SELECT table_1.segment, SUM(table_1.quantity) AS total_quantity
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_1.segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    ''',
    "8.  Average discount percentage given per region": '''
        SELECT table_0.region, AVG(table_1.discount_percent) AS avg_discount_percent
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.region;
    ''',
    "9.  Product category with the highest total profit": '''
        SELECT table_0.category, SUM(table_1.profit) AS total_profit
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.category
        ORDER BY total_profit DESC
        LIMIT 1;
    ''',
    "10. Total revenue generated per year": '''
        SELECT YEAR(table_0.order_date) AS year, 
               SUM(table_1.sale_price * table_1.quantity) AS total_revenue
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY YEAR(table_0.order_date);
    ''',
    "11. Total revenue generated per region": '''
        SELECT table_0.region, SUM(table_1.sale_price * table_1.quantity) AS total_revenue
        FROM table_1
        JOIN table_0 ON table_1.order_id = table_0.order_id
        GROUP BY table_0.region
        ORDER BY total_revenue DESC;
    ''',
    "12. Top 5 cities by total order count": '''
        SELECT table_0.city, COUNT(order_id) AS total_orders
        FROM table_0
        GROUP BY table_0.city
        ORDER BY total_orders DESC
        LIMIT 5;
    ''',
    "13. Bottom 5 cities based on total profit": '''
        SELECT table_0.city, SUM(table_1.profit) AS total_profit
        FROM table_0
        JOIN table_1 ON table_0.order_id = table_1.order_id
        GROUP BY table_0.city
        ORDER BY total_profit ASC
        LIMIT 5;
    ''',
    "14. Total orders per month": '''
        SELECT MONTH(order_date) AS month, COUNT(order_id) AS total_orders
        FROM table_0
        GROUP BY month
        ORDER BY total_orders DESC;
    ''',
    "15. Total profit per sub-category": '''
        SELECT table_0.sub_category, SUM(table_1.profit) AS total_profit
        FROM table_1
        JOIN table_0 ON table_1.order_id = table_0.order_id
        GROUP BY table_0.sub_category
        ORDER BY total_profit DESC;
    ''',
    "16. Top 3 customer segments by total spending": '''
        SELECT table_1.segment, SUM(table_1.sale_price * table_1.quantity) AS total_spent
        FROM table_1
        GROUP BY table_1.segment
        ORDER BY total_spent DESC
        LIMIT 3;
    ''',
    "17. Average discount percentage per category": '''
        SELECT table_0.category, AVG(table_1.discount_percent) AS avg_discount
        FROM table_1
        JOIN table_0 ON table_1.order_id = table_0.order_id
        GROUP BY table_0.category;
    ''',
    "18. Product with the highest total profit": '''
        SELECT table_1.product_id, SUM(table_1.profit) AS total_profit
        FROM table_1
        GROUP BY table_1.product_id
        ORDER BY total_profit DESC
        LIMIT 1;
    ''',
    "19. Most common shipping mode": '''
        SELECT table_0.ship_mode, COUNT(table_0.order_id) AS total_orders
        FROM table_0
        GROUP BY table_0.ship_mode
        ORDER BY total_orders DESC
        LIMIT 1;
    ''',
    "20. Total discount given per month": '''
        SELECT MONTH(order_date) AS month, SUM(table_1.discount) AS total_discount
        FROM table_1
        JOIN table_0 ON table_1.order_id = table_0.order_id
        GROUP BY month
        ORDER BY total_discount DESC;
    '''
}

selected_query = st.selectbox("Select a query to run:", list(query_options.keys()))


# Run the selected query

# Initialize session state
if "run_disabled" not in st.session_state:
    st.session_state.run_disabled = False
if "clear_disabled" not in st.session_state:
    st.session_state.clear_disabled = True

# Function to disable Run and enable Clear
def run_action():
    st.session_state.run_disabled = True
    st.session_state.clear_disabled = False

# Function to reset buttons
def clear_action():
    st.session_state.run_disabled = False
    st.session_state.clear_disabled = True

# Create three columns to push Clear button to the right
col1, col2, col3 = st.columns([1, 1, 5])  

with col1:
    st.button("Run", key="run_btn", disabled=st.session_state.run_disabled, on_click=run_action)

with col3:  # Moving Clear button to the rightmost column
    st.button("Clear", key="clear_btn", disabled=st.session_state.clear_disabled, on_click=clear_action)

# Display heading only when Run is clicked
if st.session_state.run_disabled:
    st.markdown(
        "<h2 style='text-align: center;'>Query Result</h2>", 
        unsafe_allow_html=True
    )

    # Ensure selected query exists before executing
    if selected_query in query_options:
        run_query(query_options[selected_query])
    else:
        st.error("Invalid query selection!")

