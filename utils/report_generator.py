import os
import matplotlib
matplotlib.use('Agg') # Safe headless execution for Flask servers
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def generate_charts(df):
    os.makedirs('static/images', exist_ok=True)
    df['date'] = pd.to_datetime(df['date'])
    
    # 1. Category Chart (Pie)
    plt.figure(figsize=(6, 4))
    cat_data = df.groupby('category')['amount'].sum()
    plt.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Spending Distribution by Category')
    plt.tight_layout()
    plt.savefig('static/images/category_pie.png')
    plt.close()

    # 2. Trend Line Chart
    plt.figure(figsize=(8, 4))
    trend_data = df.groupby('date')['amount'].sum().reset_index()
    sns.lineplot(data=trend_data, x='date', y='amount', marker='o', color='#4e73df')
    plt.title('Daily Spending Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/images/spending_trend.png')
    plt.close()