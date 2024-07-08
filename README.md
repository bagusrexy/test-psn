## How to run
Make sure you already installed **python3.8** in your machine
- pip install -r requirements.txt
- flask run --host=0.0.0.0 --port=8080

### How to Manage ORM DB 
1. make migrate file (alembic), for any change in your models
    <br>`export FLASK_APP=app.py'
    <br>`flask db migrate -d "models/migrations" -m "message"`
    <br> recheck your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
2. execute migration for your change in db
    <br>`flask db upgrade`