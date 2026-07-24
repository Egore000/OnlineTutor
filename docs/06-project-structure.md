# Project Structure

> Версия: 1.0
> Статус: Утверждено
> Документ: 06-project-structure.md

---

# 1. Назначение документа

Документ описывает структуру исходного кода проекта.

Основная цель структуры:

- простота навигации;
- минимальное количество абстракций;
- независимость модулей;
- соответствие Clean Architecture;
- удобство масштабирования.

После утверждения структура проекта считается стабильной.

---

# 2. Общая структура проекта

```
project/

├── app/
├── docs/
├── tests/
├── alembic/
├── scripts/
├── docker/
│
├── pyproject.toml
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
└── Makefile
```

---

# 3. Назначение директорий

## app/

Исходный код приложения.

---

## docs/

Вся документация проекта.

---

## tests/

Все тесты.

---

## alembic/

Миграции базы данных.

---

## docker/

Docker-конфигурация.

---

## scripts/

Вспомогательные скрипты.

Например:

```
create_admin.py

seed_demo_data.py

backup_database.py
```

---

# 4. Структура каталога app

```
app/

├── modules/
├── shared/
├── main.py
└── settings.py
```

---

## main.py

Точка входа приложения.

Здесь только:

- создание FastAPI;
- подключение роутеров;
- middleware;
- lifespan.

Никакой бизнес-логики.

---

## settings.py

Создание объекта Settings.

Чтение переменных окружения.

---

# 5. Модули

Все бизнес-функции находятся в

```
modules/
```

Структура:

```
modules/

    accounts/

    users/

    students/

    subjects/

    materials/

    lessons/

    homework/

    progress/

    ai/
```

Каждый модуль полностью изолирован.

---

# 6. Структура модуля

Каждый модуль имеет одинаковое устройство.

```
students/

├── application/
├── domain/
├── infrastructure/
└── presentation/
```

Это правило распространяется на все модули проекта.

---

# 7. Слой Presentation

```
presentation/

    router.py

    schemas.py

    dependencies.py
```

---

## router.py

FastAPI Router.

Только HTTP.

---

## schemas.py

Pydantic DTO.

Request.

Response.

---

## dependencies.py

Dependency Injection.

Получение текущего пользователя.

Проверка доступа.

---

# 8. Слой Application

```
application/

├── commands/
├── queries/
├── dto/
└── services.py
```

---

## commands/

Use Cases, изменяющие состояние системы.

Например:

```
create_student.py

update_student.py

delete_student.py
```

---

## queries/

Use Cases только для чтения.

Например:

```
get_student.py

list_students.py
```

---

## dto/

DTO, используемые между слоями.

Не зависят от FastAPI.

---

## services.py

Небольшие сервисы приложения.

Например:

координация нескольких Use Case.

---

# 9. Слой Domain

```
domain/

├── entities.py
├── value_objects.py
├── repositories.py
├── services.py
├── exceptions.py
└── events.py
```

---

## entities.py

Доменные сущности.

---

## value_objects.py

Value Objects.

---

## repositories.py

Интерфейсы Repository.

---

## services.py

Domain Services.

---

## exceptions.py

Доменные исключения.

---

## events.py

Domain Events.

---

# 10. Слой Infrastructure

```
infrastructure/

├── models.py
├── repository.py
├── mapper.py
└── services.py
```

---

## models.py

SQLAlchemy модели.

---

## repository.py

Реализация Repository.

---

## mapper.py

Преобразование

Entity ⇄ ORM Model.

---

## services.py

Интеграция с внешними сервисами.

Например:

OpenAI.

---

# 11. Shared

Общие компоненты находятся здесь.

```
shared/

├── auth/
├── config/
├── database/
├── exceptions/
├── logging/
├── storage/
├── security/
├── pagination/
├── middleware/
├── utils/
└── types/
```

---

# 12. Shared/Auth

```
auth/

jwt.py

password.py

current_user.py
```

---

# 13. Shared/Database

```
database/

base.py

session.py

factory.py
```

---

## base.py

Базовый Declarative Base.

---

## session.py

Создание AsyncSession.

---

## factory.py

Session Factory.

---

# 14. Shared/Config

```
config/

settings.py
```

Используется Pydantic Settings.

Все настройки читаются только здесь.

---

# 15. Shared/Storage

Единая работа с файлами.

```
storage/

storage.py

local.py
```

Позже можно добавить

```
s3.py
```

без изменения бизнес-логики.

---

# 16. Shared/Logging

```
logging/

config.py
```

Единая настройка логирования.

---

# 17. Shared/Exceptions

Общие исключения.

```
exceptions/

base.py

http.py
```

---

# 18. Shared/Types

Общие типы проекта.

Например

```
UserId

LessonId

HomeworkId
```

Используются TypeAlias.

---

# 19. Tests

```
tests/

├── unit/
├── integration/
├── api/
├── fixtures/
└── factories/
```

---

## unit/

Тестирование бизнес-логики.

---

## integration/

Тестирование Repository.

---

## api/

Проверка REST API.

---

## fixtures/

Pytest Fixtures.

---

## factories/

Генерация тестовых объектов.

---

# 20. Alembic

```
alembic/

versions/

env.py
```

Все миграции находятся только здесь.

---

# 21. Docs

```
docs/

00-vision.md

01-roadmap.md

02-architecture.md

03-domain-model.md

04-database.md

05-api.md

06-project-structure.md

07-coding-standards.md

08-testing.md

adr/
```

---

# 22. Правила создания новых модулей

Каждый новый модуль обязан содержать:

```
application

domain

infrastructure

presentation
```

Никаких исключений.

---

# 23. Импорт зависимостей

Разрешённые направления импортов:

```
Presentation
    ↓
Application
    ↓
Domain

Infrastructure
    ↓
Domain
```

Запрещено:

```
Domain

↓

Presentation
```

---

# 24. Naming Convention

Модули:

```
students

lessons

homework
```

---

Файлы:

```
create_student.py

list_students.py

repository.py
```

---

Классы:

```
CreateStudentUseCase

StudentRepository

Student
```

---

# 25. Размер файлов

Рекомендуемые ограничения.

| Тип | Размер |
|------|---------|
| Router | ≤300 строк |
| Use Case | ≤200 строк |
| Repository | ≤250 строк |
| Entity | ≤300 строк |
| Schema | ≤250 строк |

Если файл становится больше — стоит рассмотреть декомпозицию.

---

# 26. Добавление новой функции

При реализации новой функции необходимо соблюдать последовательность:

1. Domain
2. Application
3. Infrastructure
4. Presentation
5. Tests

Нельзя начинать с Router или ORM-модели.

---

# 27. Запрещено

В проекте запрещается:

- создавать папку `services/` в корне проекта;
- складывать все модели в один файл;
- создавать общие `BaseRepository` и `BaseService`, если они содержат бизнес-логику;
- обращаться к SQLAlchemy из Presentation;
- использовать глобальные объекты `Session`.

---

# 28. Пример структуры проекта

```
app/
│
├── modules/
│   ├── accounts/
│   ├── users/
│   ├── students/
│   ├── subjects/
│   ├── materials/
│   ├── lessons/
│   ├── homework/
│   ├── progress/
│   └── ai/
│
├── shared/
│   ├── auth/
│   ├── config/
│   ├── database/
│   ├── exceptions/
│   ├── logging/
│   ├── middleware/
│   ├── pagination/
│   ├── security/
│   ├── storage/
│   ├── types/
│   └── utils/
│
├── main.py
└── settings.py
│
tests/
│
├── unit/
├── integration/
├── api/
├── fixtures/
└── factories/
│
docs/
│
├── 00-vision.md
├── 01-roadmap.md
├── 02-architecture.md
├── 03-domain-model.md
├── 04-database.md
├── 05-api.md
├── 06-project-structure.md
├── 07-coding-standards.md
├── 08-testing.md
└── adr/
```

---

# 29. Definition of Project Structure Done

Структура проекта считается завершённой, если:

- все модули имеют одинаковую организацию;
- отсутствуют циклические зависимости;
- общие компоненты вынесены в `shared`;
- бизнес-логика находится только в слоях `domain` и `application`;
- проект легко масштабируется добавлением нового модуля без изменения существующих.

---

# 30. Главный принцип структуры проекта

> **Структура проекта должна помогать разработчику находить нужный код за секунды, а не заставлять его помнить, где что лежит.**

Каждый модуль должен быть независимым, понятным и максимально самодостаточным.
