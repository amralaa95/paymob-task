# paymob-task


## Building local

```bash
change DB_HOST ENV to localhost
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements
python manage.py migrate
python manage.py loaddata users_seed.json
python manage.py runserver


## Run tests
python manage.py test


## Building Docker compose

we use Docker compose, this will install Mysql and seed it with some data then launch the app

```bash
sudo docker-compose up --build

```
You might need to run the following command if docker has problem with permission then run above command again.
```shell
chmod +x ./run.sh
```

## Swagger


```bash
http://localhost:8000/openapi/
```

## User with role admin credentials

```bash
username = admin
password = admin
```

## Simple Steps

```bash
- Get a Token using Admin Credentials in api /login/
- Authorize by access token from above step
- Create a User with admin/normal role in api /users/
- Create/Get a Promo in api /promos/
- Update/Delete a Promo in api /promos/{id}/
- Get a Token using normal user credentials in api /login/
- Authorize by access token from above step
- Get a Promo in api /promos/
- Get a reamining points in api /points/get_points/{id}/
- Use promo points in api /points/use_promo/ 
```