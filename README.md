# API
## Prerequisites
You need docker and docker-compose to be installed on your machine
## Run
### Run docker containers
```
  docker-compose up -d
```
### Go into container shell
```
  docker exec -ti star_navi_api_1 sh
```
### Aply migrations
```
  python manage.py makemigrations
  python manage.py migrate
```
### Create user which has access to analytics and activity endpoints
```
    python manage.py shell
    from account.models import UserModel
    user = UserModel(username='username', password='password', is_staff=True)
    user.save()
```

## Postman collection
https://www.getpostman.com/collections/8284a920f21fe6bd5b02
