# Lab 5: Multi-container Application with Docker Compose

## Описание проекта
Это веб-приложение с использованием Docker Compose, включающее:
- **API на Flask** для работы с пользователями
- **PostgreSQL** для хранения данных
- **Redis** для кеширования
- **Nginx** (опционально) как reverse proxy

Приложение позволяет:
- Проверять статус приложения (`/health`)
- Проверять соединение с БД (`/db-test`)
- Проверять соединение с Redis (`/cache-test`)
- Создавать пользователей (`POST /users`)
- Получать пользователей (`GET /users`, `GET /users/:id`)

## Структура проекта
lab5-compose/
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── api/
│ ├── Dockerfile
│ ├── app.py
│ ├── requirements.txt
│ └── config.py
├── nginx/
│ └── nginx.conf
└── README.md


## Запуск проекта

1. Сборка и запуск контейнеров:
```bash
docker compose up --build -d
