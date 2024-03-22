# О проекте:
Приложение поддерживает:
 - Регистрацию
 - Аутентификацию
 - Выход из учётной записи
 - Добавление комикса
 - Возврат рейтинга комикса по его id
 - Пользовательскую оценку комикса

Что выполнено по  ТЗ:
1. На сайте комиксов  **реализована** система оценки и отображения рейтинга для **каждого** комикса
2. Рейтинг  основан на **средней** **оценке**, которую пользователи могут ставить комиксам (от 1 до 5)
3. Создана модель **Comics**
4. Создана модель **Rating**
5. Реализован роутер **/api/ratings/** с методом POST для  **создания** оценки, **обновления** среднего рейтинга комикса и **сохранения** оценки в БД.
6. Реализован роутер **/api/comics/<comic_id>/rating/** для получения **среднего** рейтинга комикса
7. Написаны **тесты** для:
	- Создания и аутентификации пользователя
	- Создания комикса
	- Создания оценки для комикса
	- Получения среднего рейтинга комикса
	- 
Так же:
-   Оставлены  **комментарии**  для лучшего понимания кода
-   Описаны  **возвращаемые**  типы данных
-   Описаны  **принимаемые**  типы данных
- Реализовано **асинхронное** подключение к БД с помощью ***asyncpg***
- Написаны **асинхронные** тесты


PS.
Файл **.env_main** нужен для **тестов** и **локального** запуска приложения
Файл 	**.env_example** нужен для развёртывания в **docker compose**
# Для запуска

1. Склонировать проект.
2. Перейти в **корень** проекта
3. Выполнить `docker compose build` и **дождаться** создания контейнеров и зависимостей
4. Выполнить `docker compose up`
5. Перейти по адресу `http://localhost:9999/docs#/`
6. Можно **вручную** протестировать контроллеры
7. Для **автоматизированных** тестов:
	- Перейти в корень проекта
	- Выполнить `pip3 install -r requirements.txt`
	- Развернуть базу данных PostgreSQL в Docker на порту **5438:5432** или **изменить** порты в файле **.env_main** на свои
	- Оставаясь в корне проекта выполнить команду `pytest tests -p no:warnings -vv`
8. Запуск основного приложения на локальной машине:
	- Из **корня** выполнить `cd src`
	- Из папки **src** выполнить `uvicorn main:app --reload`
	- Перейти по адресу `http://127.0.0.1:8000/docs#/`