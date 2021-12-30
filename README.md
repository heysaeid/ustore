## About The Project
The project is a Ustore,


#### Built With:
  - python
  - django
  - unit test
  - rabbitmq
  - celery 
  - redis
  - sqlite
  - postgresql
  - docker
   ------------------------------------
   
#### Install locally
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
```

### create superuser
```
docker-compose exec web python manage.py createsuperuser