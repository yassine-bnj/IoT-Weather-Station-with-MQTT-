import paho.mqtt.client as mqtt
import sqlite3

DB_PATH = "weather_data.db"
BROKER = "mosquitto"
TOPIC = "weather/#"

# Connect to the SQLite database
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    value REAL NOT NULL
)
''')
conn.commit()

# MQTT callback when connected
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with code", rc)
    client.subscribe(TOPIC)

# MQTT callback when a message is received
def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 2:
            return
        sensor_type = topic_parts[1]
        payload = msg.payload.decode()

        timestamp, value = payload.split(",")
        value = float(value)

        cursor.execute('''
        INSERT INTO weather_data (sensor_type, timestamp, value)
        VALUES (?, ?, ?)
        ''', (sensor_type, timestamp, value))
        conn.commit()

        print(f"Saved {sensor_type}: {value} at {timestamp}")
    except Exception as e:
        print(f"Failed to process message: {e}")

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
