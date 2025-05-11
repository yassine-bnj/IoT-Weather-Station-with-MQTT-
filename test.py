import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('weather_data.db')

# Create a cursor object
cursor = conn.cursor()

# Insert sample weather data
cursor.execute('''
    INSERT INTO weather (temperature, humidity)
    VALUES (?, ?)
''', (22.5, 60))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Sample data inserted successfully!")
