import streamlit as st

# Page config
st.set_page_config(
    page_title="Amazon India Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Amazon India: A Decade of Sales Analytics 📈🇮🇳")

# Skills & Domain
st.subheader("Skills & Tools")
st.write("Python • Pandas • Matplotlib • Seaborn • Data Cleaning • SQL • PowerBI/Streamlit • Business Intelligence • Statistical Analysis")

st.subheader("Domain")
st.write("E-Commerce Analytics")

# Problem Statement
st.subheader("🎯 Problem Statement")
st.write("""
Build a comprehensive e-commerce analytics platform using Amazon India's synthetic 10-year transactional data (2015-2025) to create an end-to-end data pipeline from raw messy data to professional business intelligence dashboards. Key features include:
- 🧹 Advanced data cleaning on messy e-commerce data with 25% quality issues
- 📊 Professional EDA visualizations with 20 analytical plots
- 🗄️ SQL database integration for cleaned data storage
- 📈 Interactive dashboards with 25-30 business-focused charts
- 💡 Strategic business insights for decision making
""")

# Business Use Cases
st.subheader("💼 Business Use Cases")
st.markdown("""
**1. 🏢 E-Commerce Platform Management**  
- Revenue trend analysis & growth forecasting  
- Product category performance & inventory planning  
- Customer segmentation for marketing  
- Geographic expansion analysis  

**2. 📊 Business Intelligence & Strategic Planning**  
- Executive dashboards for C-level decisions  
- KPI monitoring & performance tracking  
- Seasonal pattern analysis  
- Market penetration & competitive insights  

**3. 🎯 Digital Marketing & Customer Analytics**  
- Customer behavior analysis for personalization  
- Festival sales impact & ROI optimization  
- Payment method evolution tracking  
- Prime membership growth strategies  

**4. 💳 Financial & Operational Excellence**  
- Pricing strategy & revenue optimization  
- Delivery performance tracking  
- Return rate analysis & quality improvement  
- Operational efficiency & cost structure analysis  

**5. 🎓 Educational & Portfolio Development**  
- Real-world data science project for portfolio  
- Advanced Pandas operations on ~1M records  
- Professional data visualization & storytelling  
- End-to-end business intelligence skills
""")

# Approach
st.subheader("🏗 Approach")
st.markdown("""
**1. 🗂 Dataset Understanding & Analysis**  
- Analyze ~1M transactions & 2000+ products  
- Explore realistic data quality issues  
- Study Indian e-commerce market evolution  

**2. 🧹 Data Cleaning Pipeline**  
- Handle missing values & standardize formats  
- Clean geographic data & remove duplicates  
- Handle outliers appropriately  

**3. 📈 Exploratory Data Analysis (EDA)**  
- 20+ visualization challenges  
- Revenue trends, seasonality & growth analysis  
- Customer segmentation & product performance  

**4. 🗄 SQL Database Integration**  
- Design optimized schema  
- Create tables for transactions, products, customers  
- Load and validate data; SQL queries for dashboards  

**5. 📊 Interactive Dashboard Development**  
- Multi-page Streamlit app with 25-30 visualizations  
- Interactive filtering & drill-downs  
- Executive summary with actionable insights
""")

st.markdown("---")
st.caption("Project by Tanmoy Pal | E-Commerce Analytics Portfolio")
