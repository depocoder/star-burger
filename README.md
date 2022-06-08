# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

Ознакомиться с сайтом можете тут https://starburger.depocoder.xyz/

![скриншот сайта](https://i.imgur.com/wBAHlDb.png)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## [Запуск без Docker](https://github.com/depocoder/star-burger/blob/main/DEV_README.md)

## [Deploy with Docker & HTTPS](https://github.com/depocoder/star-burger/blob/main/DOCKER_DEPLOY_README.md)

## Установите [Docker и Docker-compose](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/)

# Соберите docker image's
```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
```

# Запустите dev версию
```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Проведите миграции
```shell
docker exec star_burger_web "python" "manage.py" "migrate" "--no-input"
docker exec star_burger_web "python" "manage.py" "create_admin"
```
> Логин от админки - `admin`, пароль - `123456` 


Теперь можете зайти на страницу  [http://127.0.0.1:80/](http://127.0.0.1:80/)

![](https://i.imgur.com/AOP6G4c.png)


За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).
