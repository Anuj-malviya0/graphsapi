from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__)
CORS(app)

# Load the CSV file
def load_data():
    file_path = 'water.csv'  # Ensure this path is correct for your deployment environment
    return pd.read_csv(file_path)

# Generate Plotly graphs
def generate_quantity_by_category(df):
    quantity_by_category = df.groupby('Category')['Quantity'].sum().reset_index()
    fig = px.bar(quantity_by_category, x='Category', y='Quantity', title='Quantity by Category',
                 labels={'Category': 'Category', 'Quantity': 'Quantity'}, text='Quantity')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return pio.to_html(fig, full_html=False)

def generate_items_by_status(df):
    items_by_status = df['Status'].value_counts().reset_index()
    items_by_status.columns = ['Status', 'Count']
    fig = px.pie(items_by_status, names='Status', values='Count', title='Items by Status')
    return pio.to_html(fig, full_html=False)

def generate_quantity_by_location(df):
    quantity_by_location = df.groupby('Location')['Quantity'].sum().reset_index()
    fig = px.bar(quantity_by_location, x='Location', y='Quantity', title='Quantity by Location',
                 labels={'Location': 'Location', 'Quantity': 'Quantity'}, text='Quantity')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return pio.to_html(fig, full_html=False)

@app.route('/plot/quantity_by_category')
def quantity_by_category():
    df = load_data()
    plot_html = generate_quantity_by_category(df)
    return plot_html

@app.route('/plot/items_by_status')
def items_by_status():
    df = load_data()
    plot_html = generate_items_by_status(df)
    return plot_html

@app.route('/plot/quantity_by_location')
def quantity_by_location():
    df = load_data()
    plot_html = generate_quantity_by_location(df)
    return plot_html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
