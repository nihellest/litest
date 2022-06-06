# Litest - тесты для подготовки к ЕГЭ по литературе

## Как запустить (dev)

- Подготавливаем среду

    ```bash
    git clone git@github.com:nihellest/litest.git
    cd litest
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

- Подготавливаем базу

    ```bash
    cd litest/
    python manage.py migrate
    ```

- Заливаем данные для разработки

    ```bash
    python manage.py loaddata ../dev_data.json
    ```

- Запускаем
    
    ```bash
    python manage.py runserver
    ```

## Дамп данных

Чтобы выгрузить только нужные данные &mdash; исключаем все системные модели:

```bash
python manage.py dumpdata --exclude admin --exclude auth --exclude contenttypes --exclude sessions > ../dev_data.json
```
