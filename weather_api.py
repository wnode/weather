import requests
import os
import psycopg2
from flask import Flask, jsonify

def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        print(f"Cidade: {city_name}")
        print(f"Temperatura: {temp}°C")
        print(f"Condição: {weather_desc}")
        print(f"Umidade: {humidity}%")
        print(f"Velocidade do Vento: {wind_speed} m/s")
        
        save_to_db(city_name, temp, weather_desc, humidity, wind_speed)
    else:
        print("Erro ao obter dados climáticos! Verifique a cidade ou a chave de API.")

def save_to_db(city, temp, weather_desc, humidity, wind_speed):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "seu_banco"),
        user=os.getenv("POSTGRES_USER", "seu_usuario"),
        password=os.getenv("POSTGRES_PASSWORD", "sua_senha"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100),
            temperature REAL,
            description VARCHAR(255),
            humidity INT,
            wind_speed REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute(
        "INSERT INTO weather (city, temperature, description, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s)",
        (city, temp, weather_desc, humidity, wind_speed)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Dados armazenados com sucesso no banco de dados.")

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "seu_banco"),
        user=os.getenv("POSTGRES_USER", "seu_usuario"),
        password=os.getenv("POSTGRES_PASSWORD", "sua_senha"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@app.route('/weather', methods=['GET'])
def get_weather_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city, temperature, description, humidity, wind_speed, timestamp FROM weather ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    weather_list = []
    for row in data:
        weather_list.append({
            "city": row[0],
            "temperature": row[1],
            "description": row[2],
            "humidity": row[3],
            "wind_speed": row[4],
            "timestamp": row[5]
        })
    
    return jsonify(weather_list)

if __name__ == "__main__":
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Pegando a chave de API do ambiente
    CITY = input("Digite o nome da cidade: ")
    get_weather(CITY, API_KEY)
    app.run(host="0.0.0.0", port=5000, debug=True)
