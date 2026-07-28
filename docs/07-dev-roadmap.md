# Development Roadmap

> Версия: 1.0
> Статус: Утверждено
> Документ: 09-development-plan.md

---

# Общие правила разработки

Проект разрабатывается итеративно по спринтам.

Каждый спринт должен:

- иметь одну понятную цель;
- состоять из нескольких Epic;
- завершаться Pull Request;
- проходить обязательное Code Review;
- не изменять ранее принятые архитектурные решения без веской причины.

После завершения каждого спринта состояние `main` должно быть полностью рабочим.

---

# Sprint 1. Foundation

**Цель**

Построить технический фундамент проекта.

## Epic 1. Инициализация проекта

- создание репозитория
- настройка UV
- pyproject.toml
- базовая структура проекта
- Makefile
- .gitignore
- .env.example

---

## Epic 2. Docker

- Dockerfile
- docker-compose
- PostgreSQL
- volumes
- network

---

## Epic 3. Конфигурация

- Pydantic Settings
- AppSettings
- DatabaseSettings
- JWTSettings
- единый Settings
- .env.example

---

## Epic 4. Database

- SQLAlchemy 2 Async
- Base
- Session
- Engine
- Alembic

---

## Epic 5. FastAPI

- создание приложения
- lifespan
- routers
- middleware
- exception handlers

---

## Epic 6. Healthcheck

- GET /health
- GET /ready

---

## Epic 7. Logging

- настройка логирования
- HTTP middleware
- обработка ошибок

---

## Epic 8. Security Infrastructure

- PasswordHasher
- JWTService
- базовая инфраструктура безопасности

---

## Epic 9. Code Quality

- Ruff
- MyPy
- Pytest
- Pre-commit

---

## Epic 10. CI/CD

- GitHub Actions
- автоматические проверки
- Branch Protection

---

# Sprint 2. Accounts & Authentication

**Цель**

Построить систему пользователей.

## Epic 1. Domain Model

- Account
- User
- роли

---

## Epic 2. Регистрация

- создание аккаунта
- подтверждение регистрации (без email)

---

## Epic 3. Авторизация

- JWT
- Refresh Token

---

## Epic 4. Current User

- зависимости FastAPI
- получение текущего пользователя

---

## Epic 5. Управление пользователями

- просмотр профиля
- изменение профиля

---

## Epic 6. Permissions

- Owner
- Teacher
- Student
- Parent

---

# Sprint 3. Students

**Цель**

Реализовать управление учениками.

## Epic 1. Student Aggregate

- создание
- изменение
- архивирование

---

## Epic 2. Родители

- привязка родителей

---

## Epic 3. Поиск

- фильтрация
- пагинация

---

## Epic 4. API

REST API

---

## Epic 5. Тесты

---

# Sprint 4. Subjects

**Цель**

Добавить поддержку любых предметов.

## Epic 1.

Subject

---

## Epic 2.

Создание предметов

---

## Epic 3.

Назначение предметов ученикам

---

## Epic 4.

API

---

# Sprint 5. Materials

**Цель**

Хранение учебных материалов.

## Epic 1.

Material Aggregate

---

## Epic 2.

Загрузка файлов

---

## Epic 3.

Структура материалов

---

## Epic 4.

API

---

# Sprint 6. Lessons

**Цель**

Полноценное расписание занятий.

## Epic 1.

Lesson Aggregate

---

## Epic 2.

Создание занятия

---

## Epic 3.

Перенос занятия

---

## Epic 4.

Отмена занятия

---

## Epic 5.

Календарь

---

# Sprint 7. Homework

**Цель**

Домашние задания.

## Epic 1.

Homework Aggregate

---

## Epic 2.

Создание задания

---

## Epic 3.

Прикрепление файлов

---

## Epic 4.

Отправка решения

---

## Epic 5.

Проверка преподавателем

---

# Sprint 8. Progress

**Цель**

Отслеживание прогресса.

## Epic 1.

Статистика

---

## Epic 2.

История обучения

---

## Epic 3.

Графики

---

## Epic 4.

API

---

# Sprint 9. AI

**Цель**

Интеграция искусственного интеллекта.

## Epic 1.

AI Service

---

## Epic 2.

Проверка домашних заданий

---

## Epic 3.

Генерация комментариев

---

## Epic 4.

Помощь ученику

---

# Sprint 10. Notifications

**Цель**

Система уведомлений.

## Epic 1.

Напоминания

---

## Epic 2.

Уведомления о новых ДЗ

---

## Epic 3.

Email (опционально)

---

## Epic 4.

Telegram

---

# Sprint 11. Analytics

**Цель**

CRM преподавателя.

## Epic 1.

Количество занятий

---

## Epic 2.

Доход

---

## Epic 3.

Посещаемость

---

## Epic 4.

Конверсия учеников

---

# Sprint 12. Public Platform

**Цель**

Подготовить платформу к использованию другими преподавателями.

## Epic 1.

Несколько преподавателей

---

## Epic 2.

Разделение данных

---

## Epic 3.

Приглашения

---

## Epic 4.

Настройки школы

---

# Sprint 13. Release

**Цель**

Подготовка MVP к эксплуатации.

## Epic 1.

Оптимизация

---

## Epic 2.

Безопасность

---

## Epic 3.

Документация

---

## Epic 4.

Docker Production

---

## Epic 5.

Deployment

---

# Правила выполнения

Перед переходом к следующему Epic:

- завершён текущий Epic;
- открыт Pull Request;
- успешно проходит CI;
- выполнено Code Review;
- замечания устранены;
- изменения объединены в `main` через **Squash and Merge**.

---

# Правила изменения Roadmap

После утверждения документа:

- новые функции добавляются только в конец Roadmap или Backlog;
- текущие спринты не изменяются без серьёзной причины;
- архитектурные решения не пересматриваются в процессе реализации MVP.

---

# Definition of Done проекта

Проект считается готовым к релизу MVP, если:

- реализованы все спринты;
- все модули покрыты тестами;
- документация актуальна;
- CI проходит без ошибок;
- приложение разворачивается одной командой Docker Compose;
- преподаватель может полностью вести образовательный процесс через платформу.
