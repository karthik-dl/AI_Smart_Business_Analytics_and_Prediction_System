import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast_sales(df):

    # Check required columns
    if 'Month' not in df.columns or 'Sales' not in df.columns:
        return None

    # Group monthly sales
    monthly = df.groupby('Month')['Sales'].sum().reset_index()

    X = monthly[['Month']]
    y = monthly['Sales']

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 3 months
    future_months = pd.DataFrame({
        'Month': [monthly['Month'].max() + i for i in range(1, 4)]
    })

    predictions = model.predict(future_months)

    future_months['Predicted Sales'] = predictions

    return monthly, future_months