1. Создайте и заполните .env файлы по примерам ([example.env](app%2Fexample.env), [example.env](media_app%2Fexample.env), [example.db.env](app%2Fexample.db.env))

Поля BUCKET_NAME, ACCESS_KEY и SECRET_KEY из [example.env](media_app%2Fexample.env) заполните любым плейсхолдером
2. Запустите сервис MinIO

```bash
docker compose up minio --build
```
3. Зайдите в локальную панель управления MinIO (localhost:9001), войдите в аккаунт по логину и паролю, который вписали в [example.env](media_app%2Fexample.env)
4. Создайте новый бакет и нового пользователя, название бакета а ключи внесите в [example.env](media_app%2Fexample.env)
5. Остановите docker compose и запустите все сервисы:

```bash
docker compose up --build
```

6. Все публичные операции доступны на http://localhost:8000/docs

### Дополнительно:

Запуск тестов

```bash
pip install pytest
cd tests
pytest
```