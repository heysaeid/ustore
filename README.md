## About The Project
The project is a Ustore,


#### Built With:
  - python
  - django
  - unit test
  - rabbitmq
  - celery 
  - redis
  - sqlite - postgresql
   ------------------------------------
   
#### Install locally
```bash
python -m venv env
source env/bin/activate
git clone https://github.com/heysaeid/ustore.git
cd ustore
pip install -r requirements.txt
```

Migrate database and run project:
```
python manage.py migrate
python manage.py runserver
