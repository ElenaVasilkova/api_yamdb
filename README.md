Черновой вариант. Надо исправить.

# Проект "API для Yatube"

Позволяет использовать возможности блога Yatube в сторонних приложениях черех API.

## Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

    ```
    git clone https://github.com/yandex-praktikum/kittygram_backend.git
    ```

    ```
    cd kittygram_backend
    ```

* Cоздать и активировать виртуальное окружение:

    ```
    python3.9 -m venv venv
    ```

    * Если у вас Linux/macOS

        ```
        source venv/bin/activate
        ```

    * Если у вас windows

        ```
        source venv/scripts/activate
        ```

    ```
    python3 -m pip install --upgrade pip
    ```

* Установить зависимости из файла requirements.txt:

    ```
    pip install -r requirements.txt
    ```

* Выполнить миграции:

    ```
    python3 manage.py migrate
    ```

* Запустить проект:

    ```
    python3 manage.py runserver
    ```

## Примеры запросов

### Получение публикаций

**GET** /api/v1/posts/

Response samples
```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

### Создание публикации

**POST** /api/v1/posts/

Request samples
```json
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
Response samples
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

### Получение комментариев

**GET** /api/v1/posts/{post_id}/comments/
Response samples
```json
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```

### Добавление комментария

**POST** /api/v1/posts/{post_id}/comments/
Request samples
```json
{
  "text": "string"
}
```

Response samples
```json
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

### Подписка

**POST** /api/v1/follow/

Request samples
```json
{
  "following": "string"
}
```

Response samples
```json
{
  "user": "string",
  "following": "string"
}
```

