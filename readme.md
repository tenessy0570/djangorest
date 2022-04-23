# Hi, this is my rest api project that I created to learn django rest framework.
<h3>This app was created using python 3.9 <br></h3>

### 1. [Installation](#Installation)
+ [Using docker](#using-docker)
  - [Via dockerhub](#via-dockerhub)
  - [Via github](#via-github)
+ [Without docker](#without-docker)
### 2. [About project](#about-project)
### 3. [Request routes](#request-routes)
+ [Auth actions](#auth-actions)
+ [Non-auth-requiring actions](#non-auth-requiring-actions)
+ [User actions](#user-actions)
+ [Admin actions](#admin-actions)
### 4. [Tests](#tests)

## Installation
### Using docker
*This way domain name for all requests would be:*<br>
```shell
localhost:8000/api
```
#### Via dockerhub
```shell
docker pull tenessy/django_rest
docker run -d -p 8000:8000 --rm tenessy/django_rest
```
#### Via github
```shell
mkdir djangorest_project
cd djangorest_project
git clone https://github.com/tenessy0570/djangorest.git
cd djangorest
docker build -t django_rest .
docker run -d -p 8000:8000 --rm django_rest
```
### Without docker
This way you will have to create superuser with credentials: <br>
```admin``` <br>
```admin``` <br>
```admin@admin.admin```

```shell
mkdir djangorest_project
cd djangorest_project
git clone https://github.com/tenessy0570/djangorest.git
cd djangorest
python -m venv venv
source ./venv/Scripts/activate
pip install -r requirements
cd project/restapi/

python manage.py migrate

python manage.py createsuperuser

# username: admin
# password: admin
# email: admin@admin.admin

python manage.py runserver
```
Domain name for all requests: <br>
```
127.0.0.1:8000/api
```
## About project
This app is a simple internet shop with authentication, 
admin and user actions with 
adding products to cart and submitting order. <br>
Bearer token is being used here to authenticate user.

## Request routes
### Auth actions
Register:
```ignorelang
GET /register/
```
Login:
```ignorelang
GET /login/
```
Logout:
```ignorelang
GET /logout/
```
### Non-auth-requiring actions
Get products list:
```ignorelang
GET /products/
```
### User actions
Add product to cart:
```ignorelang
POST /cart/<product_id>
```
Get cart items list:
```ignorelang
GET /cart/
```
Delete product from cart:
```ignorelang
DELETE /cart/<item_id>
```
Submit order:
```ignorelang
POST /order/
```
Get all user's orders:
```ignorelang
GET /order/
```
### Admin actions
Create new product:
```ignorelang
POST /service/
```
Delete product:
```ignorelang
DELETE /service/<product_id>
```
Edit product:
```ignorelang
PATCH /service/<product_id>
```
## Tests
Unfortunately, I was too lazy to create pytest samples but i created postman collection that works very well <br>
[!postman json file to import!](https://raw.githubusercontent.com/tenessy0570/djangorest/main/postman_collection.json) 
(import it as postman collection and run all collection when local server is up) <br>
also do not forget to import environment file
[!postman json environment file!](https://raw.githubusercontent.com/tenessy0570/djangorest/main/postman_environment.json) 
where you would change main domain 
name depending on 
the way you installed this app (localhost or 127.0.0.1) <br><br>
Talking about pytests - right now i have only auth test cases <br>
If you want to test - go to the folder with the same level as file manage.py and type:
```shell
python manage.py test api.tests
```