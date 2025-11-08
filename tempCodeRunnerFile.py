
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load model bundle
with open('model_bundle.pkl', 'rb') as f:
    bundle = pickle.load(f)

model = bundle['model']
base_date = datetime.strptime(bundle.get('base_date', '2025-09-16'), '%Y-%m-%d')

@app.route('/')
def home():
    return "Energy Forecast API is running ✅"

def make_forecast(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    future_days = (future_dates - base_date).days
    future_df = pd.DataFrame({
        'Report_Date': future_dates,
        'days_since_start': future_days
    })
    future_df['Predicted_Avg_Kwh'] = model.predict(future_df[['days_since_start']])
    return future_df

@app.route('/forecast', methods=['POST','GET'])
def forecast():
    if request.method == 'POST':
        data = request.get_json() or {}
        start_date = data.get('start_date')
        end_date = data.get('end_date')
    else:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'Provide start_date and end_date in YYYY-MM-DD format'}), 400

    df = make_forecast(start_date, end_date)
    return jsonify(df.to_dict(orient='records'))

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)