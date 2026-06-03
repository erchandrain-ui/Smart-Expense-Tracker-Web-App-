import os
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.data_handler import load_expenses, save_expense, import_csv_data
from utils.prediction import predict_next_month
from utils.report_generator import generate_charts

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/dashboard')
def dashboard():
    df = load_expenses()
    if df.empty:
        return render_template('dashboard.html', total=0, category_summary={}, recent=[])
    
    total = df['amount'].sum()
    category_summary = df.groupby('category')['amount'].sum().to_dict()
    recent = df.tail(5).to_dict(orient='records')
    return render_template('dashboard.html', total=round(total, 2), category_summary=category_summary, recent=recent)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        
        if not date or not amount:
            flash('Date and Amount are required!', 'danger')
            return redirect(url_for('add_expense'))
            
        save_expense(date, category, amount, description)
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_expense.html')

@app.route('/analytics')
def analytics():
    df = load_expenses()
    if df.empty:
        flash('Add some data first to see analytics!', 'info')
        return redirect(url_for('dashboard'))
    
    # Generate charts to static/images/
    generate_charts(df)
    return render_template('analytics.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    prediction = None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                import_csv_data(filepath)
                flash('CSV Data imported successfully!', 'success')
                return redirect(url_for('dashboard'))
        
        if 'predict' in request.form:
            prediction = predict_next_month()
            
    return render_template('reports.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)