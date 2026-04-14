from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import pickle

def train_model(df):
    df = df.select_dtypes(include=['number'])

    X = df.drop('Sales', axis=1)
    y = df['Sales']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)

    # 🔥 NEW: Feature Importance
    feature_names = X.columns.tolist()
    importance = model.feature_importances_

    # Save model
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    # 🔥 UPDATED RETURN
    return model, r2, mae, feature_names, importance


def load_saved_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model