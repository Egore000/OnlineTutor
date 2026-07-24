# API Specification

> Версия: 1.0  
> Статус: Утверждено  
> Документ: 05-api.md

---

# 1. Назначение документа

Документ описывает публичное REST API проекта.

API является единственной точкой взаимодействия между Frontend и Backend.

Все клиенты (Web, Mobile, Desktop) работают исключительно через HTTP API.

---

# 2. Архитектурные принципы

Используется REST API.

Формат данных:

```
JSON
```

Кодировка:

```
UTF-8
```

Версия API:

```
/api/v1/
```

Все новые версии публикуются отдельно.

Например:

```
/api/v2/
```

---

# 3. Формат URL

Используется множественное число.

Правильно:

```
/students

/homework

/lessons
```

Неправильно:

```
/student

/getStudents
```

---

# 4. HTTP Methods

| Метод | Назначение |
|--------|------------|
| GET | Получение данных |
| POST | Создание |
| PATCH | Частичное обновление |
| DELETE | Удаление |

PUT в MVP не используется.

---

# 5. Content-Type

Все запросы используют

```
application/json
```

Исключение:

```
multipart/form-data
```

для загрузки файлов.

---

# 6. Общий формат ответа

Успешный ответ

```json
{
  "data": {}
}
```

---

Ошибка

```json
{
  "error": {
    "code": "student_not_found",
    "message": "Student not found"
  }
}
```

---

# 7. HTTP Status Codes

| Код | Значение |
|------|----------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Validation Error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Internal Error |

---

# 8. Authentication

Используется JWT.

Access Token передается

```
Authorization: Bearer <token>
```

Все защищенные эндпоинты требуют авторизации.

---

# 9. Auth API

## POST

```
/auth/register
```

Создание аккаунта.

---

Request

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

---

Response

```json
{
  "data": {
    "id": "uuid"
  }
}
```

---

## POST

```
/auth/login
```

---

Request

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

---

Response

```json
{
  "data": {
    "access_token": "...",
    "refresh_token": "..."
  }
}
```

---

## POST

```
/auth/refresh
```

Обновление Access Token.

---

## POST

```
/auth/logout
```

Завершение сессии.

---

# 10. User API

## GET

```
/me
```

Получение собственного профиля.

---

## PATCH

```
/me
```

Обновление профиля.

---

Request

```json
{
  "first_name": "Ivan",
  "last_name": "Petrov",
  "phone": "+79999999999"
}
```

---

# 11. Student API

## GET

```
/students
```

Получение списка учеников.

---

Параметры

```
page

size

search
```

---

## POST

```
/students
```

Создание ученика.

---

Request

```json
{
  "first_name": "Alex",
  "last_name": "Ivanov",
  "phone": "+79998887766",
  "notes": "Подготовка к ЕГЭ"
}
```

---

## GET

```
/students/{student_id}
```

Получение карточки.

---

## PATCH

```
/students/{student_id}
```

Редактирование.

---

## DELETE

```
/students/{student_id}
```

Удаление.

---

# 12. Subject API

## GET

```
/subjects
```

---

## POST

```
/subjects
```

---

## GET

```
/subjects/{subject_id}
```

---

## PATCH

```
/subjects/{subject_id}
```

---

## DELETE

```
/subjects/{subject_id}
```

---

# 13. Material API

## GET

```
/materials
```

---

Фильтры

```
subject_id
```

---

## POST

```
/materials
```

Загрузка материала.

Используется

```
multipart/form-data
```

---

## GET

```
/materials/{material_id}
```

---

## DELETE

```
/materials/{material_id}
```

---

# 14. Lesson API

## GET

```
/lessons
```

---

Фильтры

```
student_id

subject_id

status

date_from

date_to
```

---

## POST

```
/lessons
```

---

Request

```json
{
  "student_id": "uuid",
  "subject_id": "uuid",
  "starts_at": "2026-07-20T12:00:00Z",
  "ends_at": "2026-07-20T13:00:00Z",
  "title": "Производная"
}
```

---

## GET

```
/lessons/{lesson_id}
```

---

## PATCH

```
/lessons/{lesson_id}
```

---

## DELETE

```
/lessons/{lesson_id}
```

---

## POST

```
/lessons/{lesson_id}/complete
```

Завершение занятия.

---

## POST

```
/lessons/{lesson_id}/cancel
```

Отмена занятия.

---

# 15. Homework API

## GET

```
/homework
```

---

Фильтры

```
student_id

lesson_id

status
```

---

## POST

```
/homework
```

---

Request

```json
{
  "lesson_id": "uuid",
  "title": "Решить задачи",
  "description": "№1-15",
  "due_at": "2026-07-25T23:59:00Z"
}
```

---

## GET

```
/homework/{homework_id}
```

---

## PATCH

```
/homework/{homework_id}
```

---

## DELETE

```
/homework/{homework_id}
```

---

# 16. Submission API

## POST

```
/homework/{homework_id}/submit
```

Отправка домашнего задания.

Используется

```
multipart/form-data
```

---

## GET

```
/submissions/{submission_id}
```

---

## PATCH

```
/submissions/{submission_id}
```

Редактирование до начала проверки.

---

# 17. Review API

## POST

```
/submissions/{submission_id}/review
```

Проверка преподавателем.

---

Request

```json
{
  "score": 95,
  "feedback": "Отличная работа."
}
```

---

## GET

```
/reviews/{review_id}
```

---

# 18. AI API

## POST

```
/ai/check-homework
```

Проверка домашнего задания.

---

Request

```json
{
  "submission_id": "uuid"
}
```

---

Response

```json
{
  "data": {
    "feedback": "...",
    "recommendation": "...",
    "estimated_score": 93
  }
}
```

---

# 19. Progress API

## GET

```
/students/{student_id}/progress
```

Получение статистики.

---

Response

```json
{
  "data": {
    "completed_lessons": 28,
    "completed_homework": 25,
    "average_score": 91.6
  }
}
```

---

# 20. Pagination

Используется Offset Pagination.

Параметры

```
page

size
```

Ответ

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 154,
    "pages": 8
  }
}
```

---

# 21. Sorting

Все коллекции поддерживают

```
sort

order
```

Пример

```
?sort=created_at&order=desc
```

---

# 22. Filtering

Допускается использование query-параметров.

Например

```
GET /students?search=Иван
```

```
GET /lessons?status=planned
```

```
GET /homework?student_id=uuid
```

---

# 23. Валидация

Все входные данные валидируются.

Ошибки возвращаются с кодом

```
422
```

Пример

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request"
  }
}
```

---

# 24. Ограничение загрузки файлов

Максимальный размер файла

```
50 MB
```

Поддерживаются

- PDF
- DOCX
- PNG
- JPG
- ZIP

Проверка MIME-типа обязательна.

---

# 25. OpenAPI

Все эндпоинты автоматически документируются через Swagger.

Документация доступна по адресу

```
/docs
```

OpenAPI JSON

```
/openapi.json
```

---

# 26. Версионирование

Несовместимые изменения публикуются только в новой версии API.

Например

```
/api/v2/
```

Старые версии поддерживаются в течение периода миграции.

---

# 27. Идемпотентность

Следующие операции считаются идемпотентными:

- GET
- PATCH (при одинаковом теле запроса)
- DELETE

Повторный вызов не должен приводить к некорректному состоянию системы.

---

# 28. Ограничение доступа

Пользователь может работать только с ресурсами, к которым имеет доступ.

Например:

- ученик не может просматривать задания другого ученика;
- ученик не может создавать занятия;
- преподаватель может управлять своими учениками.

Проверка прав доступа выполняется до выполнения бизнес-логики.

---

# 29. Стандарт именования DTO

Используются следующие соглашения.

### Request

```
CreateStudentRequest

UpdateLessonRequest

CreateHomeworkRequest
```

---

### Response

```
StudentResponse

LessonResponse

HomeworkResponse
```

---

### List

```
StudentListResponse

LessonListResponse
```

---

# 30. Definition of API Done

API считается завершённым, если:

- каждый Use Case имеет соответствующий endpoint;
- все DTO строго типизированы;
- все ошибки документированы;
- OpenAPI соответствует реализации;
- отсутствуют недокументированные эндпоинты;
- все маршруты покрыты интеграционными тестами.

---

# 31. Итоговая карта API

```
Auth
├── POST   /auth/register
├── POST   /auth/login
├── POST   /auth/refresh
└── POST   /auth/logout

Users
├── GET    /me
└── PATCH  /me

Students
├── GET    /students
├── POST   /students
├── GET    /students/{id}
├── PATCH  /students/{id}
└── DELETE /students/{id}

Subjects
├── GET    /subjects
├── POST   /subjects
├── GET    /subjects/{id}
├── PATCH  /subjects/{id}
└── DELETE /subjects/{id}

Materials
├── GET    /materials
├── POST   /materials
├── GET    /materials/{id}
└── DELETE /materials/{id}

Lessons
├── GET    /lessons
├── POST   /lessons
├── GET    /lessons/{id}
├── PATCH  /lessons/{id}
├── DELETE /lessons/{id}
├── POST   /lessons/{id}/complete
└── POST   /lessons/{id}/cancel

Homework
├── GET    /homework
├── POST   /homework
├── GET    /homework/{id}
├── PATCH  /homework/{id}
├── DELETE /homework/{id}
└── POST   /homework/{id}/submit

Submissions
├── GET    /submissions/{id}
└── PATCH  /submissions/{id}

Reviews
├── POST   /submissions/{id}/review
└── GET    /reviews/{id}

AI
└── POST   /ai/check-homework

Progress
└── GET    /students/{id}/progress
```
