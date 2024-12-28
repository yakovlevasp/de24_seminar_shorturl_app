# Сервис сокращения ссылок (Shaort URL App)

## Описание проекта
Этот сервис предоставляет API для создания коротких ссылок, их перенаправления и получения статистики. Основан на FastAPI, использует SQLite для хранения данных и легко разворачивается через Docker.

## Возможности
- **Создание коротких ссылок** (POST /shorten)
- **Перенаправление** по короткой ссылке (GET /{short_id})
- **Получение информации** о ссылке (GET /stats/{short_id})
- **Обработка коллизий** при генерации коротких ID
- **Валидация URL** через Pydantic (HttpUrl)

## Структура проекта
```
.
├── main.py           # Основное приложение FastAPI
├── models.py         # Модель базы данных (SQLAlchemy)
├── database.py       # Подключение к БД и инициализация
├── requirements.txt  # Зависимости проекта
├── Dockerfile        # Сборка Docker-образа
└── url.db            # SQLite база данных (создается автоматически)
```

## Запуск с Docker

### Шаг 1: Сборка Docker-образа
```bash
docker build -t fastapi-url-shortener .
```

### Шаг 2: Запуск контейнера
```bash
docker run -d -p 8000:80 -v shorturl_data:/app/data fastapi-url-shortener
```

### Шаг 3: Проверить работу можно запросом
```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

## API Эндпоинты
### 1. POST /shorten
- **Описание:** Создает короткую ссылку
![shorten.JPG](img%2Fshorten.JPG)

### 2. GET /{short_id}
- **Описание:** Перенаправляет на полный URL
![get_short_id.JPG](img%2Fget_short_id.JPG)

### 3. GET /stats/{short_id}
- **Описание:** Возвращает информацию о сокращенной ссылке
![get_short_id.JPG](img%2Fget_short_id.JPG)

## Описание файлов
### main.py
- Основной файл приложения. Содержит:
  - Эндпоинты API (создание, редирект, статистика)
  - Логику генерации коротких ссылок
  - Обработку исключений

### models.py
- Описание модели URLItem для базы данных.
  - `id` - первичный ключ
  - `short_id` - уникальный короткий ID
  - `full_url` - полный URL

### database.py
- Подключение к SQLite и создание сессии для работы с БД.
  - `SessionLocal` - генерация сессии
  - `Base` - базовый класс моделей

### Dockerfile
- Описание Docker-образа.
  - Установка Python-зависимостей
  - Копирование файлов приложения
  - Запуск uvicorn для FastAPI

## Зависимости
- **Python 3.9+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **Uvicorn**

### Примечание
- Данные базы хранятся в `url.db`.
- Контейнер использует том `/app/data`, чтобы данные сохранялись между запусками.
- DockerHub: https://hub.docker.com/r/yakovlevasp/shorturl-service/tags

 