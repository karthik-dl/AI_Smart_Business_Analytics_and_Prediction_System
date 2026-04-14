import streamlit as st
import pandas as pd

from src.forecasting import forecast_sales
from src.anomaly_detection import detect_anomalies
from src.report_generator import generate_report
from src.insights import generate_insights  # ✅ NEW

from src.preprocessing import load_data, clean_data
from src.model import train_model, load_saved_model
from src.model_comparison import compare_models
from src.visualization import sales_by_region, monthly_sales, category_sales

st.set_page_config(page_title="Business Analytics", layout="wide")

st.title("📊 Smart Business Analytics & Prediction System")

# Sidebar
st.sidebar.title("⚙️ Navigation")
section = st.sidebar.radio("Go to", ["Home", "Dashboard", "Prediction"])

# Upload
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if not uploaded_file:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

df = load_data(uploaded_file)
df = clean_data(df)

# ---------------- HOME ----------------
if section == "Home":
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    if st.button("Train Model"):
        model, r2, mae, feature_names, importance = train_model(df)

        st.success("Model trained!")
        st.write(f"R2 Score: {r2:.3f}")
        st.write(f"MAE: {mae:.3f}")

        # Feature Importance
        st.write("### 🔍 Feature Importance")

        feature_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importance
        }).sort_values(by="Importance", ascending=False)

        st.bar_chart(feature_df.set_index("Feature"))

# ---------------- DASHBOARD ----------------
elif section == "Dashboard":

    # ---------------- FILTERS ----------------
    st.sidebar.subheader("🔍 Filters")

    if 'Region' in df.columns:
        regions = st.sidebar.multiselect(
            "Region", df['Region'].unique(), df['Region'].unique()
        )
        df = df[df['Region'].isin(regions)]

    if 'Category' in df.columns:
        categories = st.sidebar.multiselect(
            "Category", df['Category'].unique(), df['Category'].unique()
        )
        df = df[df['Category'].isin(categories)]

    # ---------------- KPI ----------------
    st.subheader("📊 KPIs")
    col1, col2, col3 = st.columns(3)

    if 'Sales' in df.columns:
        col1.metric("Total Sales", f"{df['Sales'].sum():.2f}")
        col3.metric("Avg Sales", f"{df['Sales'].mean():.2f}")

    if 'Profit' in df.columns:
        col2.metric("Total Profit", f"{df['Profit'].sum():.2f}")

    # ---------------- AI INSIGHTS ----------------
    st.subheader("🤖 AI Insights")

    insights = generate_insights(df)

    for insight in insights:
        st.write(insight)

    # ---------------- CHARTS ----------------
    fig1 = sales_by_region(df)
    if fig1:
        st.plotly_chart(fig1)

    fig2 = monthly_sales(df)
    if fig2:
        st.plotly_chart(fig2)

    fig3 = category_sales(df)
    if fig3:
        st.plotly_chart(fig3)

    # ---------------- FORECASTING ----------------
    st.subheader("🔮 Sales Forecast (Next 3 Months)")

    result = forecast_sales(df)

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
        results = compare_models(df)
        st.dataframe(pd.DataFrame(results))

    # ---------------- ANOMALY DETECTION ----------------
    st.subheader("🚨 Anomaly Detection")

    result = detect_anomalies(df)

    if result:
        df_with_anomaly, anomalies = result

        st.write(f"🔴 Total Anomalies Detected: {len(anomalies)}")

        import plotly.express as px

        fig = px.scatter(
            df_with_anomaly,
            y='Sales',
            color=df_with_anomaly['Anomaly'].astype(str),
            title="Anomaly Detection (Red = Anomaly)"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("### 🔍 Anomaly Data")
        st.dataframe(anomalies)

    # ---------------- PDF REPORT ----------------
    st.subheader("📄 Generate Report")

    if st.button("Generate PDF Report"):

        file_path = generate_report(df)

        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="business_report.pdf",
                mime="application/pdf"
            )

# ---------------- PREDICTION ----------------
elif section == "Prediction":

    st.subheader("🤖 Sales Prediction")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if 'Sales' in numeric_cols:
        numeric_cols.remove('Sales')

    user_input = []

    for col in numeric_cols:
        val = st.number_input(f"{col}", value=0.0)
        user_input.append(val)

    if st.button("Predict"):
        try:
            model = load_saved_model()
        except:
            model, _, _, _, _ = train_model(df)

        prediction = model.predict([user_input])
        st.success(f"💰 Predicted Sales: {prediction[0]:.2f}")