# Установка и запуск

Для установки и запуска сайта на локальном компьютере необходимо выполнить следующие шаги:

- Клонировать репозиторий на свой компьютер с помощью команды `git clone https://github.com/yourusername/oncology-django.git`.
- Создать виртуальное окружение с помощью `python -m venv myenv` и активировать его `source myenv/bin/activate` (для Linux/Mac) или `myenv\Scripts\activate` (для Windows).
- Установить необходимые зависимости с помощью `pip install -r requirements.txt`.
- Выполнить миграции базы данных с помощью команды `python manage.py migrate`.
- Заполнить базу фикстурами ```python manage.py loaddata fixtures.json```.
- Запустить сервер с помощью команды ```python manage.py runserver```.
