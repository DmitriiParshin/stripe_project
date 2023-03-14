# stripe_project
## Задание
Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
* Django Модель Item с полями (name, description, price)
* API с методом GET (/buy/{id}), c помощью которого можно получить Stripe Session Id для оплаты выбранного Item.
* API с методом GET (/item/{id}), c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму
* Залить решение на Github, описать запуск в Readme.md
* Запуск используя Docker
* Использование environment variables
* Просмотр Django Моделей в Django Admin панели
* Запуск приложения на удаленном сервере, доступном для тестирования
* Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
* Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
* Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
* Реализовать не Stripe Session, а Stripe Payment Intent.
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
docker-compose exec app python manage.py migrate
```
5. Создайте суперпользователя:
```
docker-compose exec app python manage.py createsuperuser
```
6. Cоберите статику:
```
docker-compose exec app python manage.py collectstatic --no-input
```
7. Перейдите на страницу администрирования и создайте несколько товаров:  
http://localhost:8000/admin
8. Перейдите на страницу с товаром для тестирования:
http://localhost:8000/item/1