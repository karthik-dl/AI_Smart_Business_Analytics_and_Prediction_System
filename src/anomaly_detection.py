import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    if 'Sales' not in df.columns:
        return None

    data = df[['Sales']]

    model = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly'] = model.fit_predict(data)

    # -1 = anomaly, 1 = normal
    anomalies = df[df['Anomaly'] == -1]

    return df, anomalies