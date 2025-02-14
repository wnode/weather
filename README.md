# Weather API

Este projeto é uma API RESTful para obter e armazenar dados climáticos usando a API OpenWeather e PostgreSQL. A API permite buscar os dados armazenados no banco de dados.

## Tecnologias Utilizadas
- Python 3.9
- Flask
- PostgreSQL
- Docker & Docker Compose
- OpenWeather API

## Configuração do Ambiente

### 1. Clonar o repositório
```sh
git clone https://github.com/wnode/weather.git
cd weather
```

### 2. Configurar as variáveis de ambiente
Crie um arquivo `.env` e defina as seguintes variáveis:
```ini
POSTGRES_DB=weather_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432
OPENWEATHER_API_KEY=SUA_CHAVE_AQUI
```

### 3. Construir e iniciar os containers
```sh
docker-compose up --build -d
```

## Uso da API

### Coletar dados climáticos
Execute manualmente para coletar dados do clima:
```sh
docker exec -it weather_api python weather_api.py
```

### Endpoints

#### 1. Obter os últimos registros armazenados
```sh
GET /weather
```
Resposta:
```json
[
  {
    "city": "São Paulo",
    "temperature": 25.3,
    "description": "céu limpo",
    "humidity": 70,
    "wind_speed": 3.2,
    "timestamp": "2024-02-14T12:00:00"
  }
]
```

## Parar e Remover os Containers
```sh
docker-compose down
```
