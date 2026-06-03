import os
import pickle
import pandas as pd
import numpy as np
from utils.data_handler import load_expenses

MODEL_PATH = 'models/expense_predictor.pkl'

def predict_next_month():
    df = load_expenses()
    if df.empty or len(df) < 5:
        return "Not enough data historical data to generate predictions (min 5 entries needed)."
        
    try:
        df['date'] = pd.to_datetime(df['date'])
        # Target feature generation: group daily expenses
        daily = df.groupby('date')['amount'].sum().reset_index()
        daily['days_elapsed'] = (daily['date'] - daily['date'].min()).dt.days
        
        X = daily[['days_elapsed']]
        y = daily['amount']
        
        # Simple real-time update of the linear regression model
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        
        # Save updating model
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
            
        # Predict next 30 days projection
        future_days = np.array([[daily['days_elapsed'].max() + i] for i in range(1, 31)])
        predicted_daily = model.predict(future_days)
        projected_total = max(0, predicted_daily.sum())
        
        return f"${projected_total:,.2f}"
    except Exception as e:
        return f"Prediction Error: {str(e)}"