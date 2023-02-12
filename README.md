# stripe_project
## Как запустить проект:
1. Клонируйте репозиторий с проектом и перейдите в каталог с ним:
```
git clone https://github.com/DmitriiParshin/stripe_project
cd stripe_project
```
2. Создайте файл .env и заполните его как показано на примере:
```
touch .env
```
>_SECRET_KEY=YOUR_SECRET_KEY  
DB_ENGINE=YOUR_DB_ENGINE  
DB_NAME=YOUR_DB_NAME  
POSTGRES_USER=YOUR_POSTGRES_USER  
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD  
DB_HOST=YOUR_DB_HOST  
DB_PORT=YOUR_DB_PORT  
STRIPE_PUBLIC_KEY=YOUR_STRIPE_PUBLIC_KEY  
STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY  
STRIPE_WEBHOOK_SECRET=YOUR_STRIPE_WEBHOOK_SECRET_  

3. Выполните команду для создания образов и запуска в контейнере приложения и базы данных
```
docker-compose up -d --build
```
4. Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
5. Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
6. Cоберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```
7. Перейдите на страницу администрирования и создайте несколько товаров:  
http://localhost:8000/admin
8. Перейдите на страницу с товаром для тестирования:
http://localhost:8000/item/1