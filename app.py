# ============================================================
# 📊 Smart Business Analytics & Prediction System
# This app helps users:
# - Upload data
# - Analyze it with charts
# - Get AI insights
# - Predict sales
# - Forecast future trends
# - Detect anomalies
# - Download reports
# ============================================================

import streamlit as st
import pandas as pd

# Import all our modules
from src.preprocessing import load_data, clean_data
from src.model import train_model, load_saved_model
from src.model_comparison import compare_models
from src.visualization import sales_by_region, monthly_sales, category_sales
from src.forecasting import forecast_sales
from src.anomaly_detection import detect_anomalies
from src.report_generator import generate_report
from src.insights import generate_insights


# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Business Analytics", layout="wide")
st.title("📊 Smart Business Analytics & Prediction System")


# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "Prediction"])


# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if not uploaded_file:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

# Load and clean data
df = load_data(uploaded_file)
df = clean_data(df)


# ============================================================
# 🏠 HOME PAGE
# ============================================================
if page == "Home":

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    if st.button("Train Model"):

        # Train model
        model, r2, mae, feature_names, importance = train_model(df)

        st.success("Model trained successfully!")
        st.write(f"R2 Score: {r2:.3f}")
        st.write(f"MAE: {mae:.3f}")

        # Feature Importance
        st.subheader("🔍 Feature Importance")

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importance
        }).sort_values(by="Importance", ascending=False)

        st.bar_chart(feature_df.set_index("Feature"))


# ============================================================
# 📊 DASHBOARD PAGE
# ============================================================
elif page == "Dashboard":

    # Copy data so filters don’t affect original
    dashboard_df = df.copy()

    # ---------------- FILTERS ----------------
    st.sidebar.subheader("🔍 Filters")

    if 'Region' in dashboard_df.columns:
        regions = st.sidebar.multiselect(
            "Select Region",
            dashboard_df['Region'].unique(),
            default=dashboard_df['Region'].unique()
        )
        dashboard_df = dashboard_df[dashboard_df['Region'].isin(regions)]

    if 'Category' in dashboard_df.columns:
        categories = st.sidebar.multiselect(
            "Select Category",
            dashboard_df['Category'].unique(),
            default=dashboard_df['Category'].unique()
        )
        dashboard_df = dashboard_df[dashboard_df['Category'].isin(categories)]

    # ---------------- KPI ----------------
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    if 'Sales' in dashboard_df.columns:
        col1.metric("Total Sales", f"{dashboard_df['Sales'].sum():.2f}")
        col3.metric("Average Sales", f"{dashboard_df['Sales'].mean():.2f}")

    if 'Profit' in dashboard_df.columns:
        col2.metric("Total Profit", f"{dashboard_df['Profit'].sum():.2f}")

    # ---------------- AI INSIGHTS ----------------
    st.subheader("🤖 AI Insights")

    insights = generate_insights(dashboard_df)
    for i in insights:
        st.write(i)

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visualizations")

    fig1 = sales_by_region(dashboard_df)
    if fig1:
        st.plotly_chart(fig1)

    fig2 = monthly_sales(dashboard_df)
    if fig2:
        st.plotly_chart(fig2)

    fig3 = category_sales(dashboard_df)
    if fig3:
        st.plotly_chart(fig3)

    # ---------------- FORECAST ----------------
    st.subheader("🔮 Sales Forecast (Next 3 Months)")

    result = forecast_sales(dashboard_df)

    if result:
        monthly, future = result

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly['Month'],
            y=monthly['Sales'],
            mode='lines+markers',
            name='Actual Sales'
        ))

        fig.add_trace(go.Scatter(
            x=future['Month'],
            y=future['Predicted Sales'],
            mode='lines+markers',
            name='Forecast',
            line=dict(dash='dash')
        ))

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- MODEL COMPARISON ----------------
    st.subheader("🤖 Model Comparison")

    if st.button("Compare Models"):
        results = compare_models(dashboard_df)
        st.dataframe(pd.DataFrame(results))

    # ---------------- ANOMALY DETECTION ----------------
    st.subheader("🚨 Anomaly Detection")

    result = detect_anomalies(dashboard_df)

    if result:
        df_anomaly, anomalies = result

        st.write(f"🔴 Total Anomalies: {len(anomalies)}")

        import plotly.express as px

        fig = px.scatter(
            df_anomaly,
            y='Sales',
            color=df_anomaly['Anomaly'].astype(str),
            title="Anomaly Detection"
        )

        st.plotly_chart(fig)
        st.dataframe(anomalies)

    # ---------------- PDF REPORT ----------------
    st.subheader("📄 Download Report")

    if st.button("Generate Report"):

        file_path = generate_report(dashboard_df)

        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="report.pdf",
                mime="application/pdf"
            )


# ============================================================
# 🤖 PREDICTION PAGE
# ============================================================
elif page == "Prediction":

    st.subheader("🤖 Predict Sales")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if 'Sales' in numeric_cols:
        numeric_cols.remove('Sales')

    user_input = []

    for col in numeric_cols:
        val = st.number_input(f"Enter {col}", value=0.0)
        user_input.append(val)

    if st.button("Predict Sales"):

        try:
            model = load_saved_model()
        except:
            st.warning("No saved model found. Training new model...")
            model, _, _, _, _ = train_model(df)

        prediction = model.predict([user_input])

        st.success(f"💰 Predicted Sales: {prediction[0]:.2f}")