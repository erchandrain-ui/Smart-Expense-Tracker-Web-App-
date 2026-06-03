import os
import pandas as pd

DATA_FILE = 'data/expenses.csv'

def load_expenses():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return pd.DataFrame(columns=['date', 'category', 'amount', 'description'])
    return pd.read_csv(DATA_FILE)

def save_expense(date, category, amount, description):
    df = load_expenses()
    new_data = pd.DataFrame([{
        'date': date,
        'category': category,
        'amount': float(amount),
        'description': description
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def import_csv_data(filepath):
    incoming_df = pd.read_csv(filepath)
    # Ensure columns match expectations
    required_cols = ['date', 'category', 'amount', 'description']
    incoming_df = incoming_df[[col for col in required_cols if col in incoming_df.columns]]
    
    df = load_expenses()
    df = pd.concat([df, incoming_df], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)