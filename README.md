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

<img width="968" height="169" alt="Screenshot 2026-03-11 at 15 17 51" src="https://github.com/user-attachments/assets/ec3e2d0e-563f-4502-b035-7db42af5364f" />




<img width="968" height="87" alt="Screenshot 2026-03-11 at 15 16 50" src="https://github.com/user-attachments/assets/0438277d-4c25-47d1-9d51-45189c7814d6" />





