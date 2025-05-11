import paho.mqtt.client as mqtt
import time
import random
import datetime

BROKER = "mosquitto"
BASE_TOPIC = "weather"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

def read_temperature():
    hour = datetime.datetime.now().hour
    base = 22.0
    if 6 <= hour < 12:
        variation = random.uniform(0.5, 2.0)
    elif 12 <= hour < 18:
        variation = random.uniform(1.0, 3.0)
    elif 18 <= hour < 22:
        variation = random.uniform(-1.0, 1.0)
    else:
        variation = random.uniform(-2.0, 0.0)
    noise = random.uniform(-0.5, 0.5)
    return round(max(15.0, min(base + variation + noise, 35.0)), 2)

def read_humidity(temperature):
    base = 60.0
    variation = -0.2 * (temperature - 22) + random.uniform(-2, 2)
    return round(max(20.0, min(base + variation, 100.0)), 2)

def read_pressure():
    return round(random.uniform(1000, 1025), 2)

def read_wind_speed():
    return round(random.uniform(0, 15), 2)

while True:
    timestamp = datetime.datetime.now().isoformat()
    temperature = read_temperature()
    humidity = read_humidity(temperature)
    pressure = read_pressure()
    wind_speed = read_wind_speed()

    client.publish(f"{BASE_TOPIC}/temperature", f"{timestamp},{temperature}")
    client.publish(f"{BASE_TOPIC}/humidity", f"{timestamp},{humidity}")
    client.publish(f"{BASE_TOPIC}/pressure", f"{timestamp},{pressure}")
    client.publish(f"{BASE_TOPIC}/wind_speed", f"{timestamp},{wind_speed}")

    print(f"[{timestamp}] Published:")
    print(f"  → temperature: {temperature}°C")
    print(f"  → humidity: {humidity}%")
    print(f"  → pressure: {pressure} hPa")
    print(f"  → wind_speed: {wind_speed} m/s")

    time.sleep(5)
