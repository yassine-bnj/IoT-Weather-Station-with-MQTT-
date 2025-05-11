from flask import Flask, render_template
import sqlite3
import plotly.express as px
import plotly.io as pio
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)
DB_PATH = "weather_data.db"

# Function to fetch the latest data
def get_latest_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT sensor_type, timestamp, value
        FROM weather_data
        ORDER BY timestamp DESC
        LIMIT 100
    ''')
    rows = cursor.fetchall()
    conn.close()

    # Organize the data by sensor type
    data = {}
    for sensor_type, timestamp, value in rows:
        if sensor_type not in data:
            data[sensor_type] = []
        data[sensor_type].append((timestamp, value))
    return data

# Chart functions
def create_line_or_area_chart(sensor_data, sensor_type, area=False):
    df = pd.DataFrame(sensor_data, columns=["timestamp", "value"])
    fig = px.area(df, x="timestamp", y="value", title=f"{sensor_type.capitalize()} Over Time") if area else px.line(df, x="timestamp", y="value", title=f"{sensor_type.capitalize()} Over Time")
    return pio.to_html(fig, full_html=False)

def create_bar_chart(sensor_data, sensor_type):
    df = pd.DataFrame(sensor_data, columns=["timestamp", "value"])
    fig = px.bar(df, x="timestamp", y="value", title=f"{sensor_type.capitalize()} Over Time")
    return pio.to_html(fig, full_html=False)

def create_gauge_chart(value, sensor_type, max_value=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': sensor_type.capitalize()},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, max_value*0.3], 'color': "lightgreen"},
                {'range': [max_value*0.3, max_value*0.7], 'color': "yellow"},
                {'range': [max_value*0.7, max_value], 'color': "red"}
            ]
        }
    ))
    return fig.to_html(full_html=False)

def create_radar_chart(latest_values):
    categories = list(latest_values.keys())
    values = list(latest_values.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Sensor Snapshot'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title="Sensor Summary", showlegend=False)
    return fig.to_html(full_html=False)

@app.route('/')
def index():
    data = get_latest_data()

    temperature_graph = create_line_or_area_chart(data.get("temperature", []), "temperature")
    humidity_graph = create_line_or_area_chart(data.get("humidity", []), "humidity", area=True)
    pressure_graph = create_bar_chart(data.get("pressure", []), "pressure")

    wind_speed_data = data.get("wind_speed", [])
    wind_speed_latest = float(wind_speed_data[0][1]) if wind_speed_data else 0
    wind_speed_graph = create_gauge_chart(wind_speed_latest, "wind_speed", max_value=50)

    latest_values = {
        "Temperature": float(data.get("temperature", [("", 0)])[0][1]),
        "Humidity": float(data.get("humidity", [("", 0)])[0][1]),
        "Pressure": float(data.get("pressure", [("", 0)])[0][1]),
        "Wind Speed": wind_speed_latest
    }

    return render_template(
        'index.html', 
        data=data,
        temperature_graph=temperature_graph,
        humidity_graph=humidity_graph,
        pressure_graph=pressure_graph,
        wind_speed_graph=wind_speed_graph,
       
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
