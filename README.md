# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

Ознакомиться с сайтом можете тут https://starburger.depocoder.xyz/

![скриншот сайта](https://i.imgur.com/wBAHlDb.png)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Deploy with Docker & HTTPS

[Ссылка на инструкцию.](https://github.com/depocoder/star-burger/blob/main/DOCKER_DEPLOY_README.md)

## Запуск с Docker

Установите Docker и Docker-compose

[Ссылка на инструкцию.](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/)

Отдельно собирать docker images не надо, их соберет Docker Compose при первом запуске.

Запустите контейнеры:

```shell
docker-compose -f docker-compose.local.yml up -d
```

Проведите миграции:
```shell
docker exec star_burger_web "python" "manage.py" "migrate" "--no-input"
```

Cоздайте админ пользователя:
```shell
docker exec star_burger_web "python" "manage.py" "create_admin"
```

Логин от админки - `admin`, пароль - `123456`

Теперь можете зайти на страницу  [http://127.0.0.1:80/](http://127.0.0.1:80/).

![](https://i.imgur.com/AOP6G4c.png)

Настройте бэкенд:

создайте файл `.env` в каталоге `star_burger/` со следующими настройками:

- `ROLLBAR_ENVIRONMENT_NAME` — в Rollbar задаёт название окружения или инсталляции сайта;
- `ROLLBAR_ACCESS_TOKEN` — API ключ от [rollbar](https://rollbar.com/), находится в ваших проектах;
- `POSTGRES_USER` — Логин от postgres user'а;
- `POSTGRES_PASSWORD` — Пароль от postgres user'а;
- `POSTGRES_HOST` — Адрес от postgres;
- `POSTGRES_PORT` — Порт от postgres;
- `DEBUG` — Дебаг-режим; Поставьте `False`;
- `YANDEX_API_KEY` — API ключ от яндекс гео-кодера;
- `SECRET_KEY` — Секретный ключ проекта. Он отвечает за шифрование на сайте/ Например, им зашифрованы все пароли на вашем сайте;
- `ALLOWED_HOSTS` — [см; документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `STATIC_DIR_NAME` - Название директории с статикой;

## Запуск тестов
```shell
docker exec star_burger_web "python" "manage.py" "test"
```

За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).
