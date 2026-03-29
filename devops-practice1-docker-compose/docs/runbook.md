docker compose up --build  
Запуск всех сервисов с пересборкой.

docker compose up --build -d  
Запуск всех сервисов в фоне.

docker compose down  
Остановка и удаление контейнеров.

docker compose ps  
Показать статус контейнеров.

docker compose logs -f  
Показать логи всех сервисов.

curl http://localhost:3000/api/products  
Проверить список товаров.

curl -I http://localhost:3000/media/shop-images/products/laptop.svg  
Проверить доступность изображения.

docker compose exec redis redis-cli KEYS "session:*"  
Показать сессии в Redis.

docker compose exec postgres psql -U shop -d shop -c "select id, user_login, product_id, quantity, status from orders;"  
Показать заказы в PostgreSQL.

docker compose down
docker compose up --build -d  
Перезапуск проекта и проверка сохранности данных.