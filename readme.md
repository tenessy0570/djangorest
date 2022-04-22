# Hi, this is my rest api project that i created to learn django rest framework.
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