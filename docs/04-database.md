# Database Design

> Версия: 1.0  
> Статус: Утверждено  
> Документ: 04-database.md

---

# 1. Назначение документа

Документ описывает структуру базы данных проекта.

Основные цели:

- определить таблицы;
- определить связи;
- определить ограничения;
- определить правила именования;
- определить стратегию миграций.

Данный документ описывает **логическую** и **физическую** модель базы данных MVP.

---

# 2. Используемые технологии

| Компонент | Выбор |
|-----------|--------|
| СУБД | PostgreSQL 17+ |
| ORM | SQLAlchemy 2.x |
| Миграции | Alembic |
| Драйвер | asyncpg |

---

# 3. Общие принципы

## UUID

Во всех таблицах используется UUID.

```sql
id UUID PRIMARY KEY
```

Причины:

- безопаснее;
- удобно при масштабировании;
- отсутствуют проблемы с последовательностями;
- проще синхронизировать данные.

---

## UTC

Все даты хранятся в UTC.

Тип:

```sql
TIMESTAMP WITH TIME ZONE
```

---

## Soft Delete

В MVP **не используется**.

Удаление является физическим.

Если понадобится история изменений — добавим позже.

---

## Audit Fields

Практически каждая таблица содержит:

```text
created_at
updated_at
```

---

# 4. Правила именования

## Таблицы

Используется множественное число.

Примеры:

```
accounts

students

subjects

lessons

materials
```

---

## Первичный ключ

Всегда

```
id
```

---

## Внешний ключ

Формат

```
<entity>_id
```

Например

```
student_id

subject_id

lesson_id
```

---

## Индексы

Формат

```
ix_<table>_<field>
```

---

## Ограничения

Формат

```
ck_<table>_<name>
```

---

## Уникальные ограничения

```
uq_<table>_<field>
```

---

## Foreign Key

```
fk_<table>_<table>
```

---

# 5. Общая ER-диаграмма

```text
Account
    │
    ▼
Student
    │
    ├──────────────┐
    ▼              ▼
Lesson        Homework
                   │
                   ▼
             Submission
                   │
                   ▼
                Review

Subject
    │
    ▼
Material

Student
    │
    ▼
Progress
```

---

# 6. Таблица accounts

Хранит данные для аутентификации.

| Поле | Тип |
|------|-----|
| id | UUID |
| email | VARCHAR(255) |
| password_hash | TEXT |
| is_active | BOOLEAN |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

### Индексы

```
email UNIQUE
```

---

# 7. Таблица students

Карточка ученика.

| Поле | Тип |
|------|-----|
| id | UUID |
| account_id | UUID NULL |
| first_name | VARCHAR(100) |
| last_name | VARCHAR(100) |
| phone | VARCHAR(30) |
| notes | TEXT |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

Почему `account_id` nullable?

На этапе MVP преподаватель сможет создать карточку ученика ещё до регистрации ученика в системе.

---

# 8. Таблица subjects

Список предметов.

| Поле | Тип |
|------|-----|
| id | UUID |
| name | VARCHAR(100) |
| description | TEXT |

---

Примеры:

- Математика
- Физика
- Python
- Английский язык

---

# 9. Таблица materials

Учебные материалы.

| Поле | Тип |
|------|-----|
| id | UUID |
| subject_id | UUID |
| title | VARCHAR(255) |
| description | TEXT |
| file_path | TEXT |
| created_at | TIMESTAMP |

---

Связь

```
Subject 1 -> N Material
```

---

# 10. Таблица lessons

Занятия.

| Поле | Тип |
|------|-----|
| id | UUID |
| student_id | UUID |
| subject_id | UUID |
| title | VARCHAR(255) |
| description | TEXT |
| starts_at | TIMESTAMP |
| ends_at | TIMESTAMP |
| status | VARCHAR(30) |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

Статусы

```
planned

completed

cancelled
```

---

# 11. Таблица homework

Домашние задания.

| Поле | Тип |
|------|-----|
| id | UUID |
| lesson_id | UUID |
| title | VARCHAR(255) |
| description | TEXT |
| due_date | TIMESTAMP |
| created_at | TIMESTAMP |

---

Связь

```
Lesson 1 -> N Homework
```

---

# 12. Таблица submissions

Сданные домашние задания.

| Поле | Тип |
|------|-----|
| id | UUID |
| homework_id | UUID |
| student_id | UUID |
| comment | TEXT |
| submitted_at | TIMESTAMP |
| status | VARCHAR(30) |

---

Статусы

```
submitted

checking

reviewed
```

---

# 13. Таблица reviews

Проверка преподавателем.

| Поле | Тип |
|------|-----|
| id | UUID |
| submission_id | UUID |
| score | INTEGER |
| feedback | TEXT |
| ai_feedback | TEXT |
| created_at | TIMESTAMP |

---

Оценка AI хранится отдельно.

Преподаватель всегда принимает окончательное решение.

---

# 14. Таблица progress

Сводная информация об ученике.

| Поле | Тип |
|------|-----|
| id | UUID |
| student_id | UUID |
| lessons_completed | INTEGER |
| homework_completed | INTEGER |
| average_score | NUMERIC(5,2) |
| updated_at | TIMESTAMP |

---

На этапе MVP допускается денормализация этой информации для быстрого отображения статистики.

---

# 15. Связи

```
accounts

    1

    |

    | optional

    ▼

students

    |

    | N

    ▼

lessons

    |

    | N

    ▼

homework

    |

    | N

    ▼

submissions

    |

    | 1

    ▼

reviews
```

---

```
subjects

    |

    ├──── lessons

    |

    └──── materials
```

---

# 16. Индексы

Создаются следующие индексы.

```
accounts.email

students.last_name

lessons.student_id

lessons.starts_at

homework.lesson_id

submissions.homework_id

submissions.student_id

reviews.submission_id

materials.subject_id
```

---

# 17. Ограничения

## Email

Уникален.

---

## Lesson

```
starts_at < ends_at
```

---

## Review

```
score >= 0

score <= 100
```

---

## Homework

```
due_date >= created_at
```

---

# 18. Каскадное удаление

Используются следующие правила.

```
Lesson

↓

Homework

CASCADE
```

---

```
Homework

↓

Submission

CASCADE
```

---

```
Submission

↓

Review

CASCADE
```

---

Удаление ученика не должно автоматически удалять историю обучения.

Поэтому:

```
Student

↓

Lesson

RESTRICT
```

---

# 19. Миграции

Все изменения структуры базы данных выполняются только через Alembic.

Запрещается:

- изменять таблицы вручную;
- выполнять SQL напрямую в production.

---

# 20. Производительность

Для MVP дополнительных оптимизаций не требуется.

Допускается:

- денормализация только для таблицы `progress`;
- добавление индексов по мере появления реальных узких мест.

Преждевременная оптимизация запрещена.

---

# 21. Резервное копирование

На этапе MVP:

- ежедневный дамп PostgreSQL;
- хранение резервных копий не менее 7 дней.

Автоматизация выполняется на уровне инфраструктуры.

---

# 22. Будущие расширения

При дальнейшем развитии проекта планируется добавить таблицы:

- `teachers`
- `organizations`
- `parents`
- `tests`
- `questions`
- `attempts`
- `notifications`
- `payments`
- `audit_logs`

Эти таблицы **не входят в MVP** и не должны влиять на текущую структуру базы данных.

---

# 23. Итоговая схема MVP

```
accounts
    │
    ▼
students
    │
    ├──────────────┐
    ▼              ▼
lessons        progress
    │
    ▼
homework
    │
    ▼
submissions
    │
    ▼
reviews

subjects
    │
    ├──────────────┐
    ▼              ▼
materials      lessons
```

---

# 24. Definition of Database Done

База данных считается завершённой, если:

- каждая сущность доменной модели имеет соответствующую таблицу;
- все связи описаны внешними ключами;
- все ограничения реализованы;
- созданы необходимые индексы;
- структура создаётся одной миграцией Alembic;
- приложение полностью работоспособно после выполнения миграций.
