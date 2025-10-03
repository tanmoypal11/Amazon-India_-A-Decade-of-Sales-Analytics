import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px

# -----------------------------
# Database connection
# -----------------------------
try:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="amazon_user",
        password="Amazon!Pass#123",
        database="amazon_db",
        port=3306
    )
except Exception as e:
    st.error(f"Database connection error: {e}")
    conn = None

# -----------------------------
# Streamlit app settings
# -----------------------------
st.set_page_config(page_title="Amazon Business Dashboard", layout="wide")
st.title("📊 Amazon Business Dashboard")
st.markdown("---")

if conn:
    # -----------------------------
    # Question Navigation Selectbox
    # -----------------------------
    questions = [
        "1️⃣ Executive Summary Dashboard",
        "2️⃣ Real-time Business Performance Monitor",
        "3️⃣ Strategic Overview Dashboard",
        "4️⃣ Financial Performance Dashboard",
        "5️⃣ Growth Analytics Dashboard",
        "6️⃣ Revenue Trend Analysis Dashboard",
        "7️⃣ Category Performance Dashboard",
        "8️⃣ Geographic Revenue Analysis",
        "9️⃣ Festival Sales Analytics",
        "🔟 Price Optimization Dashboard",
        "1️⃣1️⃣ Customer Segmentation Dashboard",
        "1️⃣2️⃣ Customer Journey Analytics Dashboard",
        "1️⃣3️⃣ Prime Membership Analytics Dashboard",
        "1️⃣4️⃣ Customer Retention Dashboard",
        "1️⃣5️⃣ Demographics & Behavior Dashboard",
        "1️⃣6️⃣ Product Performance Dashboard",
        "1️⃣7️⃣ Brand Analytics Dashboard",
        "1️⃣8️⃣ Inventory Optimization Dashboard",
        "1️⃣9️⃣ Product Rating & Review Dashboard",
        "2️⃣0️⃣ New Product Launch Dashboard",
        "2️⃣1️⃣ Delivery Performance Dashboard",
        "2️⃣2️⃣ Payment Analytics Dashboard",
        "2️⃣3️⃣ Return & Cancellation Dashboard",
        "2️⃣4️⃣ Customer Service Dashboard",
        "2️⃣5️⃣ Supply Chain Dashboard",
        "2️⃣6️⃣ Predictive Analytics Dashboard",
        "2️⃣7️⃣ Market Intelligence Dashboard",
        "2️⃣8️⃣ Cross-selling & Upselling Dashboard",
        "2️⃣9️⃣ Seasonal Planning Dashboard",
        "3️⃣0️⃣ Business Intelligence Command Center"
    ]
    
    selected_question = st.selectbox(
        "🚀 Navigate to Specific Dashboard:",
        questions,
        index=0
    )
    
    st.markdown("---")

    # -----------------------------
    # Question 1: Executive Summary Dashboard
    # -----------------------------
    if selected_question == "1️⃣ Executive Summary Dashboard":
        st.header("1️⃣ Executive Summary Dashboard")
        try:
            query1 = """
            WITH Annual_Metrics AS (
                SELECT
                    order_year,
                    SUM(final_amount_inr) AS Raw_Revenue_INR,
                    COUNT(DISTINCT customer_id) AS Active_Customers,
                    ROUND(SUM(final_amount_inr) / COUNT(DISTINCT transaction_id), 2) AS Average_Order_Value_INR
                FROM orders
                WHERE order_year > 2020
                GROUP BY 1
            ),
            Revenue_Growth AS (
                SELECT
                    order_year,
                    Active_Customers,
                    Average_Order_Value_INR,
                    ROUND(Raw_Revenue_INR / 10000000.0, 2) AS Total_Revenue_Cores,
                    LAG(Raw_Revenue_INR, 1) OVER (ORDER BY order_year) AS Previous_Year_Revenue,
                    ROUND(
                        ((Raw_Revenue_INR - LAG(Raw_Revenue_INR, 1) OVER (ORDER BY order_year)) / LAG(Raw_Revenue_INR, 1) OVER (ORDER BY order_year)) * 100,
                        2
                    ) AS YoY_Revenue_Growth_Pct
                FROM Annual_Metrics
            ),
            Subcategory_Ranked AS (
                SELECT
                    order_year,
                    subcategory,
                    ROUND(SUM(final_amount_inr) / 10000000.0, 2) AS Subcategory_Revenue_Cores,
                    ROW_NUMBER() OVER (PARTITION BY order_year ORDER BY SUM(final_amount_inr) DESC) as rn
                FROM orders
                WHERE order_year > 2020
                GROUP BY 1, 2
            ),
            Top_Subcategory_Per_Year AS (
                SELECT
                    order_year,
                    subcategory AS Top_Subcategory_Name,
                    Subcategory_Revenue_Cores AS Final_Subcategory_Revenue_Cores
                FROM Subcategory_Ranked
                WHERE rn = 1
            )
            SELECT
                RG.order_year AS Year,
                RG.Total_Revenue_Cores,
                RG.YoY_Revenue_Growth_Pct,
                RG.Active_Customers,
                RG.Average_Order_Value_INR,
                TC.Top_Subcategory_Name,
                TC.Final_Subcategory_Revenue_Cores AS Top_Subcategory_Revenue_Cores 
            FROM Revenue_Growth RG
            JOIN Top_Subcategory_Per_Year TC
                ON RG.order_year = TC.order_year
            ORDER BY RG.order_year ASC;
            """
            df1 = pd.read_sql(query1, conn)
            
            # Display metrics for the latest year
            latest = df1.iloc[-1]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Total Revenue (₹ Cr)", f"{latest.Total_Revenue_Cores:,.2f}", f"{latest.YoY_Revenue_Growth_Pct:.2f}%")
            col2.metric("👥 Active Customers", f"{latest.Active_Customers:,}")
            col3.metric("🛒 Average Order Value (₹)", f"{latest.Average_Order_Value_INR:,.2f}")
            col4.metric("🏆 Top Subcategory", f"{latest.Top_Subcategory_Name} ({latest.Top_Subcategory_Revenue_Cores:.2f} Cr)")
            
            # Revenue trend chart
            st.subheader("Revenue Trend & YoY Growth")
            st.line_chart(df1.set_index('Year')[['Total_Revenue_Cores']])
            st.bar_chart(df1.set_index('Year')[['YoY_Revenue_Growth_Pct']])
            
        except Exception as e:
            st.warning(f"Failed to load Executive Summary Dashboard. Error: {e}")

    # -----------------------------
    # Question 2: Real-time Business Performance Monitor
    # -----------------------------
    elif selected_question == "2️⃣ Real-time Business Performance Monitor":
        st.header("2️⃣ Real-time Business Performance Monitor")
        try:
            query2 = """
            SELECT
                order_year,
                order_month,
                COUNT(DISTINCT customer_id) AS active_customers,
                COUNT(transaction_id) AS total_orders,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                SUM(quantity) AS total_quantity,
                ROUND(AVG(customer_rating), 1) AS avg_customer_rating,
                CASE
                    WHEN SUM(final_amount_inr) >= LAG(SUM(final_amount_inr)) OVER (PARTITION BY order_year ORDER BY order_month)
                    THEN 'OK'
                    ELSE 'ALERT: Revenue Down'
                END AS revenue_alert
            FROM orders
            WHERE order_year > 2020
            GROUP BY order_year, order_month
            ORDER BY order_year, order_month;
            """
            df2 = pd.read_sql(query2, conn)

            # Display current month metrics
            current = df2.iloc[-1]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Revenue (₹ Cr)", f"{current.revenue_in_crores:.2f}", current.revenue_alert)
            col2.metric("👥 Active Customers", f"{current.active_customers:,}")
            col3.metric("🛒 Total Orders", f"{current.total_orders:,}")
            col4.metric("📦 Total Quantity", f"{current.total_quantity:,}")

            # Line chart for revenue run-rate
            st.subheader("Revenue Run-rate Over Months")
            df2['Year-Month'] = df2['order_year'].astype(str) + "-" + df2['order_month'].astype(str)
            st.line_chart(df2.set_index('Year-Month')[['revenue_in_crores', 'total_orders']])
            
        except Exception as e:
            st.warning(f"Failed to load Real-time Business Performance Monitor. Error: {e}")

    # -----------------------------
    # Question 3: Strategic Overview Dashboard
    # -----------------------------
    elif selected_question == "3️⃣ Strategic Overview Dashboard":
        st.header("3️⃣ Strategic Overview Dashboard")
        try:
            query3 = """
            WITH brand_revenue AS (
                SELECT
                    order_year,
                    brand,
                    SUM(final_amount_inr) AS revenue,
                    COUNT(transaction_id) AS total_orders
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year, brand
            ),
            total_revenue_year AS (
                SELECT
                    order_year,
                    SUM(final_amount_inr) AS total_revenue
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year
            )
            SELECT
                br.order_year,
                br.brand,
                ROUND(br.revenue / 10000000, 2) AS revenue_in_crores,
                br.total_orders,
                ROUND(br.revenue / try.total_revenue * 100, 2) AS market_share_percent
            FROM brand_revenue br
            JOIN total_revenue_year try
              ON br.order_year = try.order_year
            ORDER BY br.order_year, br.revenue DESC;
            """
            df3 = pd.read_sql(query3, conn)

            # Show data
            st.subheader("📊 Market Share & Brand Positioning")
            st.dataframe(df3, use_container_width=True)

            # KPI-style snapshot for latest year
            latest_year = df3["order_year"].max()
            latest_data = df3[df3["order_year"] == latest_year]

            st.markdown(f"### Latest Year ({latest_year}) Competitive Positioning")
            col1, col2, col3 = st.columns(3)
            top_brand = latest_data.iloc[0]
            col1.metric("🏆 Top Brand", f"{top_brand['brand']}", f"{top_brand['market_share_percent']}%")
            col2.metric("💰 Revenue (₹ Cr)", f"{top_brand['revenue_in_crores']:.2f}")
            col3.metric("📦 Orders", f"{top_brand['total_orders']:,}")

            # Market Share Trend Chart
            st.subheader("📈 Market Share Trends by Brand")
            pivot_df = df3.pivot(index="order_year", columns="brand", values="market_share_percent").fillna(0)
            st.line_chart(pivot_df)

            # Revenue Competitive Matrix (latest year)
            st.subheader("🏢 Competitive Positioning Matrix (Revenue vs Market Share)")
            st.scatter_chart(latest_data, x="revenue_in_crores", y="market_share_percent", size="total_orders", color="brand")

        except Exception as e:
            st.warning(f"Failed to load Strategic Overview Dashboard. Error: {e}")

    # -----------------------------
    # Question 4: Financial Performance Dashboard
    # -----------------------------
    elif selected_question == "4️⃣ Financial Performance Dashboard":
        st.header("4️⃣ Financial Performance Dashboard")
        try:
            query4 = """
            SELECT
                order_year,
                subcategory,
                ROUND(SUM(original_price_inr * quantity) / 10000000, 2) AS gross_sales_crores,
                ROUND(SUM(original_price_inr * discount_percent/100 * quantity) / 10000000, 2) AS discount_given_crores,
                ROUND(SUM(final_amount_inr) / 10000000, 2) AS net_revenue_crores,
                ROUND(SUM(delivery_charges) / 10000000, 2) AS delivery_charges_crores
            FROM orders
            WHERE order_year > 2020
            GROUP BY order_year, subcategory
            ORDER BY order_year, net_revenue_crores DESC;
            """
            df4 = pd.read_sql(query4, conn)
        
            # Show data
            st.subheader("📊 Financial Breakdown by Subcategory")
            st.dataframe(df4, use_container_width=True)
        
            # KPI snapshot (overall)
            st.subheader("💰 Key Financial Metrics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Gross Sales (₹ Cr)", f"{df4['gross_sales_crores'].sum():,.2f}")
            col2.metric("Net Revenue (₹ Cr)", f"{df4['net_revenue_crores'].sum():,.2f}")
            col3.metric("Discounts Given (₹ Cr)", f"{df4['discount_given_crores'].sum():,.2f}")
            col4.metric("Delivery Charges (₹ Cr)", f"{df4['delivery_charges_crores'].sum():,.2f}")
        
            # Revenue Breakdown by Subcategory (Stacked Bar)
            st.subheader("🛒 Revenue Breakdown by Subcategory (Year-wise)")
            pivot_rev = df4.pivot(index="order_year", columns="subcategory", values="net_revenue_crores").fillna(0)
            st.bar_chart(pivot_rev, use_container_width=True)
        
            # Cost Structure (Discounts & Delivery Charges vs Revenue)
            st.subheader("⚙️ Cost Structure Components")
            df_cost = df4.groupby("order_year")[["discount_given_crores", "delivery_charges_crores", "net_revenue_crores"]].sum()
            st.area_chart(df_cost, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Financial Performance Dashboard. Error: {e}")

    # -----------------------------
    # Question 5: Growth Analytics Dashboard
    # -----------------------------
    elif selected_question == "5️⃣ Growth Analytics Dashboard":
        st.header("5️⃣ Growth Analytics Dashboard")
        try:
            query5 = """
            WITH customer_growth AS (
                SELECT
                    order_year,
                    COUNT(DISTINCT customer_id) AS active_customers
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year
            ),
            product_expansion AS (
                SELECT
                    order_year,
                    COUNT(DISTINCT product_id) AS unique_products
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year
            ),
            revenue_growth AS (
                SELECT
                    order_year,
                    ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_crores
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year
            )
            SELECT
                cg.order_year,
                cg.active_customers,
                pe.unique_products,
                rg.revenue_crores
            FROM customer_growth cg
            JOIN product_expansion pe ON cg.order_year = pe.order_year
            JOIN revenue_growth rg ON cg.order_year = rg.order_year
            ORDER BY cg.order_year;
            """
            df5 = pd.read_sql(query5, conn)

            # Show data
            st.subheader("📈 Growth Metrics Over Years")
            st.dataframe(df5, use_container_width=True)

            # KPI snapshot (latest year)
            latest = df5.iloc[-1]
            col1, col2, col3 = st.columns(3)
            col1.metric("👥 Customers", f"{latest.active_customers:,}")
            col2.metric("📦 Unique Products", f"{latest.unique_products:,}")
            col3.metric("💰 Revenue (₹ Cr)", f"{latest.revenue_crores:.2f}")

            # Growth Trends
            st.subheader("📊 Growth Trends")
            st.line_chart(df5.set_index("order_year")[["active_customers", "unique_products", "revenue_crores"]])

        except Exception as e:
            st.warning(f"Failed to load Growth Analytics Dashboard. Error: {e}")

    # -----------------------------
    # Question 6: Revenue Trend Analysis Dashboard with Time Period Selector
    # -----------------------------
    elif selected_question == "6️⃣ Revenue Trend Analysis Dashboard":
        st.header("6️⃣ Revenue Trend Analysis Dashboard")
        try:
            time_period = st.selectbox(
                "Select Time Period for Revenue Analysis",
                ["Yearly", "Quarterly", "Monthly", "Seasonal Variation", "Forecast"]
            )
        
            if time_period == "Yearly":
                query = """
                SELECT
                    order_year,
                    ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                    ROUND(SUM(final_amount_inr)/NULLIF(LAG(SUM(final_amount_inr)) OVER (ORDER BY order_year),1) - 1, 4) * 100 AS yoy_growth_pct
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year
                ORDER BY order_year;
                """
                df = pd.read_sql(query, conn)
                st.subheader("📅 Yearly Revenue Trend")
                st.line_chart(df.set_index("order_year")["revenue_in_crores"])
                st.dataframe(df, use_container_width=True)
        
            elif time_period == "Quarterly":
                query = """
                SELECT
                    order_year,
                    order_quarter,
                    ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                    ROUND(
                        (SUM(final_amount_inr) - LAG(SUM(final_amount_inr)) OVER (ORDER BY order_year, order_quarter))
                        / NULLIF(LAG(SUM(final_amount_inr)) OVER (ORDER BY order_year, order_quarter),0)
                        * 100, 2
                    ) AS qoq_growth_pct
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year, order_quarter
                ORDER BY order_year, order_quarter;
                """
                df = pd.read_sql(query, conn)
                st.subheader("📊 Quarterly Revenue Trend")
                df["quarter_label"] = df["order_year"].astype(str) + " Q" + df["order_quarter"].astype(str)
                st.line_chart(df.set_index("quarter_label")["revenue_in_crores"])
                st.dataframe(df, use_container_width=True)
        
            elif time_period == "Monthly":
                query = """
                SELECT
                    order_year,
                    order_month,
                    ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                    ROUND(SUM(final_amount_inr)/NULLIF(LAG(SUM(final_amount_inr)) OVER (PARTITION BY order_year ORDER BY order_month),1) - 1, 4) * 100 AS mon_growth_pct
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_year, order_month
                ORDER BY order_year, order_month;
                """
                df = pd.read_sql(query, conn)
                st.subheader("📆 Monthly Revenue Trend")
                df["month_label"] = df["order_year"].astype(str) + "-" + df["order_month"].astype(str).str.zfill(2)
                st.line_chart(df.set_index("month_label")["revenue_in_crores"])
                st.dataframe(df, use_container_width=True)
        
            elif time_period == "Seasonal Variation":
                query = """
                SELECT
                    order_month,
                    ROUND(SUM(final_amount_inr)/10000000, 2) AS avg_revenue_in_crores,
                    COUNT(DISTINCT order_year) AS years_considered
                FROM orders
                WHERE order_year > 2020
                GROUP BY order_month
                ORDER BY order_month;
                """
                df = pd.read_sql(query, conn)
                st.subheader("🌸 Seasonal Revenue Variation")
                st.bar_chart(df.set_index("order_month")["avg_revenue_in_crores"])
                st.dataframe(df, use_container_width=True)
        
            elif time_period == "Forecast":
                query = """
                WITH monthly_avg AS (
                    SELECT
                        order_month,
                        AVG(final_amount_inr) AS avg_monthly_revenue
                    FROM orders
                    WHERE order_year > 2020
                    GROUP BY order_month
                )
                SELECT
                    m.order_month,
                    ROUND(m.avg_monthly_revenue/1000000, 2) AS projected_revenue_in_lakhs
                FROM monthly_avg m
                ORDER BY m.order_month;
                """
                df = pd.read_sql(query, conn)
                st.subheader("🔮 Simple Revenue Forecast (Next 3 Months / Monthly Avg)")
                st.bar_chart(df.set_index("order_month")["projected_revenue_in_lakhs"])
                st.dataframe(df, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Revenue Trend Analysis Dashboard. Error: {e}")

    # -----------------------------
    # Question 7: Category Performance Dashboard
    # -----------------------------
    elif selected_question == "7️⃣ Category Performance Dashboard":
        st.header("7️⃣ Category Performance Dashboard (Subcategory)")
        try:
            # Revenue Contribution by Subcategory
            query1 = """
            SELECT
                subcategory,
                ROUND(SUM(final_amount_inr)/100000, 2) AS revenue_in_lakhs,
                ROUND(SUM(final_amount_inr)/SUM(SUM(final_amount_inr)) OVER (), 4) * 100 AS revenue_share_pct
            FROM orders
            WHERE order_year > 2020
            GROUP BY subcategory
            ORDER BY revenue_in_lakhs DESC;
            """
            df_revenue_share = pd.read_sql(query1, conn)
            st.subheader("📊 Revenue Contribution by Subcategory")
            st.bar_chart(df_revenue_share.set_index("subcategory")["revenue_in_lakhs"])
            st.dataframe(df_revenue_share, use_container_width=True)
        
            # Yearly Revenue Growth by Subcategory
            query2 = """
            SELECT
                order_year,
                ROUND(SUM(CASE WHEN subcategory='Smartphones' THEN final_amount_inr ELSE 0 END)/100000, 2) AS Smartphones_revenue_in_lakhs,
                ROUND(SUM(CASE WHEN subcategory='Laptops' THEN final_amount_inr ELSE 0 END)/100000, 2) AS Laptops_revenue_in_lakhs,
                ROUND(SUM(CASE WHEN subcategory='Tablets' THEN final_amount_inr ELSE 0 END)/100000, 2) AS Tablets_revenue_in_lakhs,
                ROUND(SUM(CASE WHEN subcategory='Smart Watch' THEN final_amount_inr ELSE 0 END)/100000, 2) AS SmartWatch_revenue_in_lakhs,
                ROUND(SUM(CASE WHEN subcategory='Audio' THEN final_amount_inr ELSE 0 END)/100000, 2) AS Audio_revenue_in_lakhs,
                ROUND(SUM(CASE WHEN subcategory='TV & Entertainment' THEN final_amount_inr ELSE 0 END)/100000, 2) AS TV_Entertainment_revenue_in_lakhs
            FROM orders
            WHERE order_year > 2020
            GROUP BY order_year
            ORDER BY order_year;
            """
            df_yearly_growth = pd.read_sql(query2, conn)
            st.subheader("📈 Yearly Revenue by Subcategory")
            st.line_chart(df_yearly_growth.set_index("order_year"))
            st.dataframe(df_yearly_growth, use_container_width=True)
        
            # Market Share Change by Subcategory
            query3 = """
            SELECT
                order_year,
                ROUND(SUM(CASE WHEN subcategory='Smartphones' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS Smartphones_market_share_pct,
                ROUND(SUM(CASE WHEN subcategory='Laptops' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS Laptops_market_share_pct,
                ROUND(SUM(CASE WHEN subcategory='Tablets' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS Tablets_market_share_pct,
                ROUND(SUM(CASE WHEN subcategory='Smart Watch' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS SmartWatch_market_share_pct,
                ROUND(SUM(CASE WHEN subcategory='Audio' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS Audio_market_share_pct,
                ROUND(SUM(CASE WHEN subcategory='TV & Entertainment' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS TV_Entertainment_market_share_pct
            FROM orders
            WHERE order_year > 2020
            GROUP BY order_year
            ORDER BY order_year;
            """
            df_market_share = pd.read_sql(query3, conn)
            st.subheader("📊 Market Share Change by Subcategory")
            st.area_chart(df_market_share.set_index("order_year"))
            st.dataframe(df_market_share, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Category Performance Dashboard. Error: {e}")

    # -----------------------------
    # Question 8: Geographic Revenue Analysis
    # -----------------------------
    elif selected_question == "8️⃣ Geographic Revenue Analysis":
        st.header("8️⃣ Geographic Revenue Analysis Dashboard")
        try:
            # 1️⃣ State-wise Revenue
            query_state = """
            SELECT
                customer_state,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                COUNT(DISTINCT customer_id) AS total_customers,
                COUNT(transaction_id) AS total_orders
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_state
            ORDER BY revenue_in_crores DESC;
            """
            df_state = pd.read_sql(query_state, conn)
            st.subheader("📍 State-wise Revenue")
            st.dataframe(df_state, use_container_width=True)
            st.bar_chart(df_state.set_index("customer_state")["revenue_in_crores"])
        
            # 2️⃣ City-wise Revenue
            query_city = """
            SELECT
                customer_state,
                customer_city,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                COUNT(DISTINCT customer_id) AS total_customers,
                COUNT(transaction_id) AS total_orders
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_state, customer_city
            ORDER BY customer_state, revenue_in_crores DESC;
            """
            df_city = pd.read_sql(query_city, conn)
            st.subheader("🏙️ City-wise Revenue (Top Cities per State)")
            st.dataframe(df_city, use_container_width=True)
        
            # 3️⃣ Tier-wise Revenue Analysis
            query_tier = """
            SELECT
                customer_tier,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                COUNT(*) AS total_orders
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_tier
            ORDER BY revenue_in_crores DESC;
            """
            df_tier = pd.read_sql(query_tier, conn)
            st.subheader("📊 Customer Tier-wise Revenue")
            st.dataframe(df_tier, use_container_width=True)
            st.bar_chart(df_tier.set_index("customer_tier")["revenue_in_crores"])
        
            # 4️⃣ Yearly State-wise Revenue Trend
            query_year_state = """
            SELECT
                order_year,
                customer_state,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                COUNT(DISTINCT customer_id) AS total_customers
            FROM orders
            WHERE order_year > 2020
            GROUP BY order_year, customer_state
            ORDER BY order_year, revenue_in_crores DESC;
            """
            df_year_state = pd.read_sql(query_year_state, conn)
            st.subheader("📈 Yearly State-wise Revenue Trend")
            pivot_state = df_year_state.pivot(index="order_year", columns="customer_state", values="revenue_in_crores").fillna(0)
            st.line_chart(pivot_state)
        
            # 5️⃣ Market Penetration Proxy
            query_penetration = """
            WITH customer_state_summary AS (
                SELECT
                    customer_id,
                    customer_state,
                    MAX(order_year) AS last_order_year
                FROM orders
                WHERE order_year > 2020
                GROUP BY customer_id, customer_state
            )
            SELECT
                customer_state,
                COUNT(customer_id) AS total_customers,
                SUM(CASE WHEN last_order_year = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS active_customers_current_year,
                ROUND(
                    SUM(CASE WHEN last_order_year = YEAR(CURDATE()) THEN 1 ELSE 0 END) / COUNT(customer_id) * 100,
                    2
                ) AS penetration_pct
            FROM customer_state_summary
            GROUP BY customer_state
            ORDER BY penetration_pct DESC;
            """
            df_penetration = pd.read_sql(query_penetration, conn)
            st.subheader("🗺️ Market Penetration by State")
            st.dataframe(df_penetration, use_container_width=True)
            st.bar_chart(df_penetration.set_index("customer_state")["penetration_pct"])
        
        except Exception as e:
            st.warning(f"Failed to load Geographic Revenue Analysis Dashboard. Error: {e}")

    # -----------------------------
    # Question 9: Festival Sales Analytics
    # -----------------------------
    elif selected_question == "9️⃣ Festival Sales Analytics":
        st.header("9️⃣ Festival Sales Analytics Dashboard")
        try:
            query_festival = """
            SELECT
                order_year,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS total_festival_revenue_in_crores,
                COUNT(transaction_id) AS total_orders,
                COUNT(DISTINCT customer_id) AS total_customers,
                ROUND(SUM(final_amount_inr)/NULLIF(COUNT(transaction_id),0), 2) AS avg_order_value_in_inr,
                SUM(CASE WHEN is_festival_sale=1 THEN 1 ELSE 0 END) AS festival_orders_count,
                ROUND(SUM(CASE WHEN is_prime_member=1 THEN final_amount_inr ELSE 0 END)/NULLIF(SUM(final_amount_inr),0) * 100, 2) AS prime_revenue_share_pct
            FROM orders
            WHERE is_festival_sale = 1 AND order_year > 2020
            GROUP BY order_year
            ORDER BY order_year;
            """
            df_festival = pd.read_sql(query_festival, conn)
        
            # Show table
            st.subheader("🎉 Festival Sales Metrics by Year")
            st.dataframe(df_festival, use_container_width=True)
        
            # KPI-style snapshot for latest year
            latest_year = df_festival["order_year"].max()
            latest_data = df_festival[df_festival["order_year"] == latest_year]
            st.markdown(f"### Latest Festival Year ({latest_year}) Highlights")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Total Revenue (₹ Cr)", f"{latest_data['total_festival_revenue_in_crores'].values[0]:.2f}")
            col2.metric("🛒 Total Orders", f"{latest_data['total_orders'].values[0]:,}")
            col3.metric("👥 Active Customers", f"{latest_data['total_customers'].values[0]:,}")
            col4.metric("🏆 Prime Revenue Share (%)", f"{latest_data['prime_revenue_share_pct'].values[0]:.2f}")
        
            # Revenue Trend Chart
            st.subheader("📈 Festival Revenue Trend Over Years")
            st.line_chart(df_festival.set_index("order_year")["total_festival_revenue_in_crores"])
        
            # Avg Order Value Trend
            st.subheader("🛍️ Average Order Value Trend")
            st.line_chart(df_festival.set_index("order_year")["avg_order_value_in_inr"])
        
            # Orders Count Trend
            st.subheader("📊 Festival Orders Count Trend")
            st.bar_chart(df_festival.set_index("order_year")["festival_orders_count"])
        
        except Exception as e:
            st.warning(f"Failed to load Festival Sales Analytics Dashboard. Error: {e}")

    # -----------------------------
    # Question 10: Price Optimization Dashboard
    # -----------------------------
    elif selected_question == "🔟 Price Optimization Dashboard":
        st.header("🔟 Price Optimization Dashboard")
        try:
            # Discount Effectiveness
            query_discount = """
            SELECT
                ROUND(discount_percent,0) AS discount_pct_bucket,
                COUNT(*) AS total_orders,
                SUM(quantity) AS total_quantity_sold,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores,
                ROUND(AVG(final_amount_inr),2) AS avg_order_value_in_inr
            FROM orders
            WHERE discount_percent IS NOT NULL AND order_year > 2020
            GROUP BY discount_pct_bucket
            ORDER BY discount_pct_bucket;
            """
            df_discount = pd.read_sql(query_discount, conn)
        
            st.subheader("💸 Discount Effectiveness")
            st.dataframe(df_discount, use_container_width=True)
        
            # Discount Metrics Chart
            st.subheader("📊 Revenue vs Discount %")
            st.bar_chart(df_discount.set_index("discount_pct_bucket")["revenue_in_crores"])
        
            st.subheader("📈 Avg Order Value vs Discount %")
            st.line_chart(df_discount.set_index("discount_pct_bucket")["avg_order_value_in_inr"])
        
            # Price vs Quantity (Elasticity)
            query_price_qty = """
            SELECT
                discounted_price_inr,
                SUM(quantity) AS total_quantity_sold,
                ROUND(SUM(final_amount_inr)/10000000, 2) AS revenue_in_crores
            FROM orders
            WHERE order_year > 2020
            GROUP BY discounted_price_inr
            ORDER BY discounted_price_inr;
            """
            df_price_qty = pd.read_sql(query_price_qty, conn)
        
            st.subheader("💰 Price vs Quantity Sold (Elasticity)")
            st.dataframe(df_price_qty, use_container_width=True)
        
            # Price Elasticity Charts
            st.subheader("📊 Total Quantity Sold vs Discounted Price")
            st.line_chart(df_price_qty.set_index("discounted_price_inr")["total_quantity_sold"])
        
            st.subheader("📈 Revenue vs Discounted Price")
            st.line_chart(df_price_qty.set_index("discounted_price_inr")["revenue_in_crores"])
        
        except Exception as e:
            st.warning(f"Failed to load Price Optimization Dashboard. Error: {e}")

    # -----------------------------
    # Question 11: Customer Segmentation Dashboard
    # -----------------------------
    elif selected_question == "1️⃣1️⃣ Customer Segmentation Dashboard":
        st.header("1️⃣1️⃣ Customer Segmentation Dashboard")
        try:
            query_rfm = """
            SELECT
                customer_id,
                COUNT(transaction_id) AS frequency,
                SUM(final_amount_inr) AS monetary_value,
                DATEDIFF(MAX(order_date), MIN(order_date)) AS recency_days
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_id
            """
            df_rfm = pd.read_sql(query_rfm, conn)
            
            st.subheader("📊 RFM Metrics")
            st.dataframe(df_rfm.head(50), use_container_width=True)
            
            # RFM summary KPIs
            st.markdown("### 🔹 RFM Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Avg Recency (Days)", f"{df_rfm['recency_days'].mean():.1f}")
            col2.metric("Avg Frequency", f"{df_rfm['frequency'].mean():.1f}")
            col3.metric("Avg Monetary Value (₹)", f"{df_rfm['monetary_value'].mean():.2f}")
        
        except Exception as e:
            st.warning(f"Failed to load Customer Segmentation Dashboard. Error: {e}")

    # -----------------------------
    # Question 12: Customer Journey Analytics Dashboard
    # -----------------------------
    elif selected_question == "1️⃣2️⃣ Customer Journey Analytics Dashboard":
        st.header("1️⃣2️⃣ Customer Journey Analytics Dashboard")
        try:
            query_journey = """
            SELECT
                customer_id,
                MIN(order_date) AS first_order_date,
                MAX(order_date) AS last_order_date,
                COUNT(DISTINCT category) AS categories_purchased,
                COUNT(transaction_id) AS total_orders
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_id
            """
            df_journey = pd.read_sql(query_journey, conn)
            
            st.subheader("📊 Customer Journey Metrics")
            st.dataframe(df_journey.head(50), use_container_width=True)
            
            st.subheader("📈 Customer Lifecycle")
            st.line_chart(df_journey.set_index("customer_id")["total_orders"])
        
        except Exception as e:
            st.warning(f"Failed to load Customer Journey Dashboard. Error: {e}")

    # -----------------------------
    # Question 13: Prime Membership Analytics Dashboard
    # -----------------------------
    elif selected_question == "1️⃣3️⃣ Prime Membership Analytics Dashboard":
        st.header("1️⃣3️⃣ Prime Membership Analytics Dashboard")
        try:
            query_prime = """
            SELECT
                is_prime_member,
                COUNT(DISTINCT customer_id) AS total_customers,
                SUM(final_amount_inr)/10000000 AS revenue_in_crores,
                ROUND(AVG(customer_rating), 2) AS avg_customer_rating
            FROM orders
            WHERE order_year > 2020
            GROUP BY is_prime_member
            """
            df_prime = pd.read_sql(query_prime, conn)
            
            st.subheader("📊 Prime vs Non-Prime Metrics")
            st.dataframe(df_prime, use_container_width=True)
            
            st.subheader("📈 Revenue Comparison")
            st.bar_chart(df_prime.set_index("is_prime_member")["revenue_in_crores"])
        
        except Exception as e:
            st.warning(f"Failed to load Prime Membership Dashboard. Error: {e}")

    # -----------------------------
    # Question 14: Customer Retention Dashboard
    # -----------------------------
    elif selected_question == "1️⃣4️⃣ Customer Retention Dashboard":
        st.header("1️⃣4️⃣ Customer Retention Dashboard")
        try:
            # -----------------------------
            # Part 1: Customer Churn Overview
            # -----------------------------
            cutoff_date = '2025-09-01'
            churn_days = 180
        
            query_churn = f"""
            WITH cust_agg AS (
                SELECT
                    o.customer_id,
                    COUNT(DISTINCT o.transaction_id) AS total_orders,
                    ROUND(SUM(o.final_amount_inr), 2) AS total_spend,
                    ROUND(AVG(o.final_amount_inr), 2) AS avg_order_value,
                    MAX(o.order_date) AS last_order_date,
                    MIN(o.order_date) AS first_order_date
                FROM orders o
                WHERE o.order_year > 2020
                GROUP BY o.customer_id
            )
            SELECT
                ca.customer_id,
                ca.total_orders,
                ca.total_spend,
                ca.avg_order_value,
                DATEDIFF('{cutoff_date}', ca.last_order_date) AS recency_days,
                DATEDIFF(ca.last_order_date, ca.first_order_date) AS tenure_days,
                CASE
                    WHEN ca.last_order_date < DATE_SUB('{cutoff_date}', INTERVAL {churn_days} DAY) THEN 1
                    ELSE 0
                END AS churn_label
            FROM cust_agg ca
            ORDER BY ca.customer_id;
            """
            df_churn = pd.read_sql(query_churn, conn)
        
            st.subheader("📊 Customer Churn Overview")
            st.dataframe(df_churn.head(50), use_container_width=True)
        
            # KPI Metrics
            total_customers = df_churn.shape[0]
            churned_customers = df_churn['churn_label'].sum()
            retained_customers = total_customers - churned_customers
        
            st.markdown("### 🔹 Churn Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("👥 Total Customers", f"{total_customers:,}")
            col2.metric("⚠️ Churned Customers", f"{churned_customers:,}", f"{churned_customers/total_customers*100:.2f}%")
            col3.metric("✅ Retained Customers", f"{retained_customers:,}", f"{retained_customers/total_customers*100:.2f}%")
        
            st.subheader("Churn Distribution")
            churn_counts = df_churn['churn_label'].value_counts().rename({0:'Active',1:'Churned'})
            st.bar_chart(churn_counts)

            # -----------------------------
            # Part 2: Retention Strategies Effectiveness
            # -----------------------------
            query_retention = f"""
            WITH cust_agg AS (
                SELECT
                    o.customer_id,
                    MAX(o.order_date) AS last_order_date,
                    AVG(o.discount_percent) AS avg_discount,
                    MAX(o.is_prime_member) AS is_prime_member
                FROM orders o
                WHERE o.order_year > 2020
                GROUP BY o.customer_id
            ),
            cust_status AS (
                SELECT
                    ca.customer_id,
                    ca.is_prime_member,
                    ROUND(ca.avg_discount, 2) AS avg_discount,
                    CASE 
                        WHEN ca.last_order_date < DATE_SUB('{cutoff_date}', INTERVAL {churn_days} DAY) THEN 1 
                        ELSE 0 
                    END AS churn_label
                FROM cust_agg ca
            )
            SELECT
                CASE WHEN is_prime_member = 1 THEN 'Prime Member' ELSE 'Non-Prime' END AS customer_type,
                ROUND(AVG(avg_discount), 2) AS avg_discount_given,
                COUNT(*) AS total_customers,
                SUM(churn_label) AS churned_customers,
                ROUND(SUM(churn_label) / COUNT(*) * 100, 2) AS churn_rate_pct,
                ROUND((COUNT(*) - SUM(churn_label)) / COUNT(*) * 100, 2) AS retention_rate_pct
            FROM cust_status
            GROUP BY is_prime_member;
            """
            df_retention = pd.read_sql(query_retention, conn)
        
            st.subheader("📊 Retention Strategies Effectiveness")
            st.dataframe(df_retention, use_container_width=True)
        
            st.markdown("### 🔹 Retention vs Churn Rates by Customer Type")
            st.bar_chart(df_retention.set_index('customer_type')[['retention_rate_pct','churn_rate_pct']])
        
        except Exception as e:
            st.warning(f"Failed to load Customer Retention Dashboard. Error: {e}")

    # -----------------------------
    # Question 15: Demographics & Behavior Dashboard
    # -----------------------------
    elif selected_question == "1️⃣5️⃣ Demographics & Behavior Dashboard":
        st.header("1️⃣5️⃣ Demographics & Behavior Dashboard")
        try:
            query_demo = """
            SELECT
                customer_age_group,
                customer_tier,
                COUNT(DISTINCT customer_id) AS total_customers,
                SUM(final_amount_inr)/10000000 AS revenue_in_crores
            FROM orders
            WHERE order_year > 2020
            GROUP BY customer_age_group, customer_tier
            ORDER BY revenue_in_crores DESC
            """
            df_demo = pd.read_sql(query_demo, conn)
            
            st.subheader("📊 Customer Demographics Metrics")
            st.dataframe(df_demo.head(50), use_container_width=True)
            
            st.subheader("📈 Revenue by Age Group")
            pivot_demo = df_demo.pivot(index="customer_age_group", columns="customer_tier", values="revenue_in_crores").fillna(0)
            st.bar_chart(pivot_demo)
        
        except Exception as e:
            st.warning(f"Failed to load Demographics Dashboard. Error: {e}")

    # -----------------------------
    # Question 16: Product Performance Dashboard
    # -----------------------------
    elif selected_question == "1️⃣6️⃣ Product Performance Dashboard":
        st.header("16️⃣ Product Performance Dashboard")
        try:
            query16 = """
            SELECT product_id, product_name, subcategory, brand, quantity, final_amount_inr, customer_id
            FROM orders
            WHERE order_year > 2020
            """
            df16_raw = pd.read_sql(query16, conn)
        
            # Aggregate in Python for safety
            df16 = df16_raw.groupby(['product_id','product_name','subcategory','brand']).agg(
                total_units_sold=('quantity', 'sum'),
                revenue_cr=('final_amount_inr', lambda x: round(x.sum()/10000000, 2)),
                total_customers=('customer_id', 'nunique')
            ).reset_index().sort_values('revenue_cr', ascending=False).head(50)
        
            st.dataframe(df16, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Product Performance Dashboard. Error: {e}")

    # -----------------------------
    # Question 17: Brand Analytics Dashboard
    # -----------------------------
    elif selected_question == "1️⃣7️⃣ Brand Analytics Dashboard":
        st.header("17️⃣ Brand Analytics Dashboard")
        try:
            query17 = """
            SELECT brand, quantity, final_amount_inr, customer_id
            FROM orders
            WHERE order_year > 2020
            """
            df17_raw = pd.read_sql(query17, conn)
        
            df17 = df17_raw.groupby('brand').agg(
                total_units_sold=('quantity', 'sum'),
                revenue_cr=('final_amount_inr', lambda x: round(x.sum()/10000000, 2)),
                total_customers=('customer_id', 'nunique')
            ).reset_index().sort_values('revenue_cr', ascending=False).head(20)
        
            st.dataframe(df17, use_container_width=True)

        except Exception as e:
            st.warning(f"Failed to load Brand Analytics Dashboard. Error: {e}")

    # -----------------------------
    # Question 18: Inventory Optimization Dashboard
    # -----------------------------
    elif selected_question == "1️⃣8️⃣ Inventory Optimization Dashboard":
        st.header("18️⃣ Inventory Optimization Dashboard")
        try:
            query18 = """
            SELECT product_id, product_name, subcategory, order_month, quantity
            FROM orders
            WHERE order_year > 2020
            """
            df18_raw = pd.read_sql(query18, conn)
        
            df18 = df18_raw.groupby(['product_id','product_name','subcategory']).agg(
                total_sold=('quantity', 'sum'),
                avg_monthly_sold=('quantity', 'mean')
            ).reset_index().sort_values('total_sold', ascending=False).head(50)
        
            st.dataframe(df18, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Inventory Optimization Dashboard. Error: {e}")

    # -----------------------------
    # Question 19: Product Rating & Review Dashboard
    # -----------------------------
    elif selected_question == "1️⃣9️⃣ Product Rating & Review Dashboard":
        st.header("19️⃣ Product Rating & Review Dashboard")
        try:
            query19 = """
            SELECT product_id, product_name, product_rating
            FROM orders
            WHERE product_rating IS NOT NULL AND order_year > 2020
            """
            df19_raw = pd.read_sql(query19, conn)
        
            df19 = df19_raw.groupby(['product_id','product_name']).agg(
                avg_rating=('product_rating', 'mean'),
                total_reviews=('product_rating', 'count')
            ).reset_index().sort_values('avg_rating', ascending=False).head(50)
        
            st.dataframe(df19, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load Product Rating & Review Dashboard. Error: {e}")

    # -----------------------------
    # Question 20: New Product Launch Dashboard
    # -----------------------------
    elif selected_question == "2️⃣0️⃣ New Product Launch Dashboard":
        st.header("20️⃣ New Product Launch Dashboard")
        try:
            query20 = """
            SELECT product_id, product_name, order_year, SUM(quantity) AS units_sold, SUM(final_amount_inr)/10000000 AS revenue_cr
            FROM orders
            WHERE order_year > 2020
            GROUP BY product_id, product_name, order_year
            ORDER BY order_year, revenue_cr DESC
            """
            df20 = pd.read_sql(query20, conn)
            st.dataframe(df20, use_container_width=True)
        
        except Exception as e:
            st.warning(f"Failed to load New Product Launch Dashboard. Error: {e}")

    # -----------------------------
    # Question 21: Delivery Performance Dashboard
    # -----------------------------
    elif selected_question == "2️⃣1️⃣ Delivery Performance Dashboard":
        st.header("21️⃣ Delivery Performance Dashboard")
        try:
            query21 = "SELECT order_year, order_month, customer_state, delivery_days, transaction_id FROM orders WHERE order_year > 2020;"
            df21 = pd.read_sql(query21, conn)
        
            # Metrics
            avg_delivery = df21.groupby(['order_year', 'order_month'])['delivery_days'].mean().reset_index()
            on_time_rate = (df21['delivery_days'] <= 5).mean() * 100  # Assuming <=5 days is on-time
        
            st.metric("⏱ Average Delivery Days", f"{df21['delivery_days'].mean():.2f}")
            st.metric("✅ On-time Delivery Rate (%)", f"{on_time_rate:.2f}")
        
            # Charts
            st.subheader("Avg Delivery Days Over Time")
            avg_delivery['Year-Month'] = avg_delivery['order_year'].astype(str) + "-" + avg_delivery['order_month'].astype(str)
            st.line_chart(avg_delivery.set_index('Year-Month')['delivery_days'])
        
            st.subheader("Delivery Days Distribution")
            st.bar_chart(df21['delivery_days'].value_counts().sort_index())
        except Exception as e:
            st.warning(f"Failed to load Delivery Performance Dashboard. Error: {e}")

    # -----------------------------
    # Question 22: Payment Analytics Dashboard
    # -----------------------------
    elif selected_question == "2️⃣2️⃣ Payment Analytics Dashboard":
        st.header("2️⃣2️⃣ Payment Analytics Dashboard")
        try:
            # -----------------------------
            # Part 1: Payment Method Preferences & Performance
            # -----------------------------
            query_payment_pref = """
            SELECT
                payment_method,
                COUNT(*) AS total_transactions,
                ROUND(SUM(final_amount_inr), 2) AS total_amount,
                ROUND(AVG(final_amount_inr), 2) AS avg_transaction_value,
                ROUND(COUNT(*) / (SELECT COUNT(*) FROM orders WHERE order_year > 2020) * 100, 2) AS pct_of_total_transactions
            FROM orders
            WHERE order_year > 2020
            GROUP BY payment_method
            ORDER BY total_transactions DESC;
            """
            df_payment_pref = pd.read_sql(query_payment_pref, conn)
        
            st.subheader("💳 Payment Method Preferences")
            st.dataframe(df_payment_pref, use_container_width=True)
        
            # KPI summary
            total_txn = df_payment_pref["total_transactions"].sum()
            total_amount = df_payment_pref["total_amount"].sum()

            col1, col2 = st.columns(2)
            col1.metric("Total Transactions", f"{total_txn:,}")
            col2.metric("Total Amount (₹)", f"{total_amount:,.2f}")
        
            st.markdown("### 🔹 Transactions Share by Method")
            st.bar_chart(df_payment_pref.set_index("payment_method")["pct_of_total_transactions"])
        
            # -----------------------------
            # Part 2: Monthly Payment Trends
            # -----------------------------
            query_payment_trends = """
            SELECT
                YEAR(order_date) AS year,
                MONTH(order_date) AS month,
                payment_method,
                COUNT(*) AS transactions_count,
                ROUND(SUM(final_amount_inr), 2) AS total_amount,
                ROUND(AVG(final_amount_inr), 2) AS avg_transaction_value
            FROM orders
            WHERE order_year > 2020
            GROUP BY YEAR(order_date), MONTH(order_date), payment_method
            ORDER BY year, month, payment_method;
            """
            df_payment_trends = pd.read_sql(query_payment_trends, conn)
        
            st.subheader("📈 Monthly Payment Trends")
            st.dataframe(df_payment_trends.head(50), use_container_width=True)

            # Prepare pivot for visualization
            df_trend_pivot = df_payment_trends.pivot_table(
                index=["year","month"], 
                columns="payment_method", 
                values="transactions_count", 
                aggfunc="sum",
                fill_value=0
            ).reset_index()
        
            df_trend_pivot["year_month"] = df_trend_pivot["year"].astype(str) + "-" + df_trend_pivot["month"].astype(str)
        
            st.markdown("### 🔹 Transaction Trends by Payment Method")
            st.line_chart(df_trend_pivot.set_index("year_month").drop(columns=["year","month"]))
        
        except Exception as e:
            st.warning(f"Failed to load Payment Analytics Dashboard. Error: {e}")

    # -----------------------------
    # Question 23: Return & Cancellation Dashboard
    # -----------------------------
    elif selected_question == "2️⃣3️⃣ Return & Cancellation Dashboard":
        st.header("2️⃣3️⃣ Return & Cancellation Dashboard")
        try:
            # -----------------------------
            # Part 1: Category-wise Return & Cancellation Impact
            # -----------------------------
            query_return_cancel = """
            SELECT
                subcategory,
                COUNT(*) AS total_orders,
                SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders,
                SUM(CASE WHEN return_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
                ROUND(SUM(CASE WHEN return_status = 'Returned' THEN final_amount_inr ELSE 0 END), 2) AS return_value,
                ROUND(SUM(CASE WHEN return_status = 'Cancelled' THEN final_amount_inr ELSE 0 END), 2) AS cancel_value,
                ROUND(SUM(CASE WHEN return_status = 'Returned' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS return_rate_pct,
                ROUND(SUM(CASE WHEN return_status = 'Cancelled' THEN final_amount_inr ELSE 0 END) / SUM(final_amount_inr) * 100, 2) AS cancel_rate_pct,
                ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
                ROUND(AVG(product_rating), 2) AS avg_product_rating
            FROM orders
            WHERE order_year > 2020
            GROUP BY subcategory
            ORDER BY return_rate_pct DESC;
            """
            df_return_cancel = pd.read_sql(query_return_cancel, conn)

            st.subheader("📊 Category-wise Return & Cancellation Impact")
            st.dataframe(df_return_cancel, use_container_width=True)
        
            # KPI summary
            total_orders = df_return_cancel["total_orders"].sum()
            total_returns = df_return_cancel["returned_orders"].sum()
            total_cancels = df_return_cancel["cancelled_orders"].sum()
            total_loss_value = df_return_cancel["return_value"].sum() + df_return_cancel["cancel_value"].sum()
        
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Orders", f"{total_orders:,}")
            col2.metric("Returned Orders", f"{total_returns:,}")
            col3.metric("Cancelled Orders", f"{total_cancels:,}")
            col4.metric("Total Loss Value (₹)", f"{total_loss_value:,.2f}")
        
            # -----------------------------
            # Part 2: Visualization
            # -----------------------------
            st.subheader("📉 Return & Cancellation Rates by Category")
            chart_data = df_return_cancel.set_index("subcategory")[["return_rate_pct", "cancel_rate_pct"]]
            st.bar_chart(chart_data)
        
        except Exception as e:
            st.warning(f"Failed to load Return & Cancellation Dashboard. Error: {e}")

    # -----------------------------
    # Question 24: Customer Service Dashboard
    # -----------------------------
    elif selected_question == "2️⃣4️⃣ Customer Service Dashboard":
        st.header("2️⃣4️⃣ Customer Service Dashboard")
        try:
            # -----------------------------
            # Part 1: Overall Service Quality Summary
            # -----------------------------
            query_service_summary = """
            SELECT
                ROUND(AVG(customer_rating), 2) AS avg_customer_satisfaction,
                COUNT(CASE WHEN return_status LIKE 'Returned%' THEN 1 END) AS total_returns,
                COUNT(CASE WHEN return_status LIKE 'Cancelled%' THEN 1 END) AS total_cancellations,
                ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
                ROUND(SUM(CASE WHEN delivery_days > 7 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS delayed_delivery_pct
            FROM orders
            WHERE order_year > 2020;
            """
            df_service_summary = pd.read_sql(query_service_summary, conn)
        
            st.subheader("📊 Overall Service Quality Summary")
            st.dataframe(df_service_summary, use_container_width=True)

            # KPI metrics
            avg_rating = df_service_summary["avg_customer_satisfaction"].iloc[0]
            total_returns = df_service_summary["total_returns"].iloc[0]
            total_cancellations = df_service_summary["total_cancellations"].iloc[0]
            avg_delivery = df_service_summary["avg_delivery_days"].iloc[0]
            delayed_pct = df_service_summary["delayed_delivery_pct"].iloc[0]
        
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Avg Satisfaction ⭐", avg_rating)
            col2.metric("Total Returns", f"{total_returns:,}")
            col3.metric("Total Cancellations", f"{total_cancellations:,}")
            col4.metric("Avg Delivery Days", f"{avg_delivery:.1f}")
            col5.metric("Delayed Deliveries (%)", f"{delayed_pct:.2f}%")
        
            # -----------------------------
            # Part 2: Service Quality Trends (Monthly)
            # -----------------------------
            query_service_trends = """
            SELECT
                YEAR(order_date) AS year,
                MONTH(order_date) AS month,
                ROUND(AVG(customer_rating), 2) AS avg_monthly_rating,
                ROUND(SUM(CASE WHEN return_status LIKE 'Returned%' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS return_rate_pct,
                ROUND(SUM(CASE WHEN return_status LIKE 'Cancelled%' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS cancel_rate_pct
            FROM orders
            WHERE order_year > 2020
            GROUP BY YEAR(order_date), MONTH(order_date)
            ORDER BY year, month;
            """
            df_service_trends = pd.read_sql(query_service_trends, conn)

            st.subheader("📈 Monthly Service Quality Trends")
            st.dataframe(df_service_trends.head(50), use_container_width=True)
        
            # Prepare chart
            df_service_trends["year_month"] = df_service_trends["year"].astype(str) + "-" + df_service_trends["month"].astype(str)
        
            st.markdown("### 🔹 Customer Rating Trend")
            st.line_chart(df_service_trends.set_index("year_month")[["avg_monthly_rating"]])
        
            st.markdown("### 🔹 Return vs Cancel Rates (%)")
            st.line_chart(df_service_trends.set_index("year_month")[["return_rate_pct", "cancel_rate_pct"]])
        
        except Exception as e:
            st.warning(f"Failed to load Customer Service Dashboard. Error: {e}")

    # -----------------------------
    # Question 25: Supply Chain Dashboard
    # -----------------------------
    elif selected_question == "2️⃣5️⃣ Supply Chain Dashboard":
        st.header("2️⃣5️⃣ Supply Chain Dashboard")
        try:
            # -----------------------------
            # Part 1: Supplier Performance Summary
            # -----------------------------
            query_supplier_summary = """
            SELECT
                brand AS supplier,
                COUNT(*) AS total_orders,
                SUM(quantity) AS total_units_supplied,
                ROUND(SUM(final_amount_inr), 2) AS total_revenue,
                ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
                ROUND(SUM(CASE WHEN delivery_days > 7 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS late_delivery_pct,
                ROUND(SUM(CASE WHEN return_status = 'Returned' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS return_rate_pct,
                ROUND(AVG(customer_rating), 2) AS avg_customer_rating
            FROM orders
            WHERE order_year > 2020
            GROUP BY brand
            HAVING total_orders > 50
            ORDER BY late_delivery_pct ASC, return_rate_pct ASC;
            """
            df_supplier_summary = pd.read_sql(query_supplier_summary, conn)
        
            st.subheader("📊 Supplier Performance Summary")
            st.dataframe(df_supplier_summary, use_container_width=True)
        
            # KPI snapshot for top supplier
            top_supplier = df_supplier_summary.iloc[0]
            st.markdown(f"### 🔹 Top Supplier: {top_supplier['supplier']}")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Orders", f"{top_supplier['total_orders']:,}")
            col2.metric("Total Units Supplied", f"{top_supplier['total_units_supplied']:,}")
            col3.metric("Avg Delivery Days", f"{top_supplier['avg_delivery_days']:.1f}")
            col4.metric("Return Rate (%)", f"{top_supplier['return_rate_pct']:.2f}%")
        
            # -----------------------------
            # Part 2: Revenue Contribution per Supplier
            # -----------------------------
            query_revenue_supplier = """
            SELECT
                brand AS supplier,
                COUNT(*) AS total_orders,
                SUM(quantity) AS total_units_supplied,
                ROUND(SUM(final_amount_inr), 2) AS total_revenue,
                ROUND(AVG(final_amount_inr), 2) AS avg_order_value
            FROM orders
            WHERE order_year > 2020
            GROUP BY brand
            ORDER BY total_revenue DESC;
            """
            df_revenue_supplier = pd.read_sql(query_revenue_supplier, conn)

            st.subheader("💰 Revenue Contribution per Supplier")
            st.dataframe(df_revenue_supplier, use_container_width=True)
        
            # Revenue pie chart
            st.markdown("### 🔹 Revenue Share by Supplier")
            st.plotly_chart(
                px.pie(df_revenue_supplier.head(10), names="supplier", values="total_revenue", title="Top 10 Suppliers by Revenue")
            )
        
            # -----------------------------
            # Part 3: Monthly Delivery Reliability Trends
            # -----------------------------
            query_delivery_trends = """
            SELECT
                YEAR(order_date) AS year,
                MONTH(order_date) AS month,
                brand AS supplier,
                COUNT(*) AS total_orders,
                ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
                ROUND(SUM(CASE WHEN delivery_days > 7 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS late_delivery_pct
            FROM orders
            WHERE order_year > 2020
            GROUP BY YEAR(order_date), MONTH(order_date), brand
            ORDER BY year, month, supplier;
            """
            df_delivery_trends = pd.read_sql(query_delivery_trends, conn)

            st.subheader("📈 Monthly Delivery Reliability Trends")
            # Pivot for visualization
            df_delivery_pivot = df_delivery_trends.pivot_table(
                index=["year","month"], columns="supplier", values="late_delivery_pct", fill_value=0
            ).reset_index()
            df_delivery_pivot["year_month"] = df_delivery_pivot["year"].astype(str) + "-" + df_delivery_pivot["month"].astype(str)
            st.line_chart(df_delivery_pivot.set_index("year_month").drop(columns=["year","month"]))
        
        except Exception as e:
            st.warning(f"Failed to load Supply Chain Dashboard. Error: {e}")

    # -----------------------------
    # Question 26: Predictive Analytics Dashboard
    # -----------------------------
    elif selected_question == "2️⃣6️⃣ Predictive Analytics Dashboard":
        st.header("26️⃣ Predictive Analytics Dashboard")
        try:
            query26 = "SELECT order_date, customer_id, product_id, quantity, final_amount_inr FROM orders WHERE order_year > 2020;"
            df26 = pd.read_sql(query26, conn)
        
            # Simple Sales Forecast: rolling 7-day average
            df26['order_date'] = pd.to_datetime(df26['order_date'])
            daily_sales = df26.groupby('order_date')['final_amount_inr'].sum().reset_index()
            daily_sales['rolling_avg'] = daily_sales['final_amount_inr'].rolling(7).mean()
        
            st.metric("💰 Total Revenue", f"{daily_sales['final_amount_inr'].sum():,.0f}")
            st.subheader("Sales Forecast (7-day rolling average)")
            st.line_chart(daily_sales.set_index('order_date')[['final_amount_inr', 'rolling_avg']])
        
            # Simple churn estimation: customers with no purchase in last 90 days
            latest_date = df26['order_date'].max()
            churn_customers = df26.groupby('customer_id')['order_date'].max()
            churn_rate = (churn_customers < (latest_date - pd.Timedelta(days=90))).mean() * 100
            st.metric("📉 Estimated Churn Rate (%)", f"{churn_rate:.2f}")
        except Exception as e:
            st.warning(f"Failed to load Predictive Analytics Dashboard. Error: {e}")

    # -----------------------------
    # Question 27: Market Intelligence Dashboard
    # -----------------------------
    elif selected_question == "2️⃣7️⃣ Market Intelligence Dashboard":
        st.header("27️⃣ Market Intelligence Dashboard")
        try:
            query27 = "SELECT order_year, brand, subcategory, final_amount_inr FROM orders WHERE order_year > 2020;"
            df27 = pd.read_sql(query27, conn)
        
            st.subheader("Revenue by Brand")
            revenue_brand = df27.groupby('brand')['final_amount_inr'].sum() / 10000000
            st.bar_chart(revenue_brand)
        
            st.subheader("Revenue by Subcategory")
            revenue_subcat = df27.groupby('subcategory')['final_amount_inr'].sum() / 10000000
            st.bar_chart(revenue_subcat)
        
            st.subheader("Top 5 Brands by Revenue")
            st.dataframe(revenue_brand.sort_values(ascending=False).head(5))
        except Exception as e:
            st.warning(f"Failed to load Market Intelligence Dashboard. Error: {e}")

    # -----------------------------
    # Question 28: Cross-selling & Upselling Dashboard
    # -----------------------------
    elif selected_question == "2️⃣8️⃣ Cross-selling & Upselling Dashboard":
        st.header("28️⃣ Cross-selling & Upselling Dashboard")
        try:
            query28 = "SELECT customer_id, product_id, subcategory FROM orders WHERE order_year > 2020;"
            df28 = pd.read_sql(query28, conn)
        
            # Simple product association count
            cross_sell = df28.groupby(['customer_id', 'subcategory']).size().reset_index(name='count')
            top_subcat = cross_sell.groupby('subcategory')['count'].sum().sort_values(ascending=False)
            
            st.subheader("Top Subcategories Bought Together")
            st.bar_chart(top_subcat.head(10))
        
            st.subheader("Customer Product Diversity")
            customer_diversity = df28.groupby('customer_id')['subcategory'].nunique()
            st.bar_chart(customer_diversity.value_counts().sort_index())
        except Exception as e:
            st.warning(f"Failed to load Cross-selling & Upselling Dashboard. Error: {e}")

    # -----------------------------
    # Question 29: Seasonal Planning Dashboard
    # -----------------------------
    elif selected_question == "2️⃣9️⃣ Seasonal Planning Dashboard":
        st.header("29️⃣ Seasonal Planning Dashboard")
        try:
            query29 = "SELECT order_date, subcategory, quantity, final_amount_inr FROM orders WHERE order_year > 2020;"
            df29 = pd.read_sql(query29, conn)
        
            df29['order_date'] = pd.to_datetime(df29['order_date'])
            df29['month'] = df29['order_date'].dt.month
        
            st.subheader("Monthly Sales Trend")
            monthly_sales = df29.groupby('month')['final_amount_inr'].sum() / 10000000
            st.bar_chart(monthly_sales)
        
            st.subheader("Monthly Quantity Sold by Subcategory")
            monthly_qty = df29.groupby(['month', 'subcategory'])['quantity'].sum().unstack().fillna(0)
            st.line_chart(monthly_qty)
        except Exception as e:
            st.warning(f"Failed to load Seasonal Planning Dashboard. Error: {e}")

    # -----------------------------
    # Question 30: Business Intelligence Command Center
    # -----------------------------
    elif selected_question == "3️⃣0️⃣ Business Intelligence Command Center":
        st.header("30️⃣ Business Intelligence Command Center")
        try:
            query30 = "SELECT order_date, customer_id, subcategory, final_amount_inr, quantity, payment_method FROM orders WHERE order_year > 2020;"
            df30 = pd.read_sql(query30, conn)
        
            st.subheader("Key Metrics Overview")
            st.metric("💰 Total Revenue (₹ Cr)", f"{df30['final_amount_inr'].sum()/10000000:.2f}")
            st.metric("👥 Total Customers", f"{df30['customer_id'].nunique():,}")
            st.metric("🛒 Total Orders", f"{len(df30):,}")
            st.metric("📦 Total Quantity Sold", f"{df30['quantity'].sum():,}")
        
            st.subheader("Revenue by Subcategory")
            st.bar_chart(df30.groupby('subcategory')['final_amount_inr'].sum()/10000000)
        
            st.subheader("Revenue by Payment Method")
            st.bar_chart(df30.groupby('payment_method')['final_amount_inr'].sum()/10000000)
        
            st.subheader("Daily Revenue Trend")
            df30['order_date'] = pd.to_datetime(df30['order_date'])
            daily_revenue = df30.groupby('order_date')['final_amount_inr'].sum()/10000000
            st.line_chart(daily_revenue)
        except Exception as e:
            st.warning(f"Failed to load Business Intelligence Command Center. Error: {e}")

    else:
        st.info("🚀 Select a dashboard from the dropdown above to get started!")

else:
    st.error("❌ Unable to connect to the database. Please check your connection settings.")