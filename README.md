# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения.

## Технологии

- Python 3
- Django 2.2
- Django REST Framework
- SQLite3
- Simple JWT

## Как запустить проект:
* Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
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
* Management-команда, добавляющая данные в БД через Django ORM

В папке с файлом manage.py выполнить команду:
```
python manage.py convert_csv
```
* Запустить проект:
```
python3 manage.py runserver
```
## Документация

После запуска проекта документация для работы с API доступна по адресу: http://127.0.0.1:8000/redoc/.
