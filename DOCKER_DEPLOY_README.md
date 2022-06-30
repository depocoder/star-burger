# Инструкция по деплою на сервер

## Процесс деплоя

Купите домен и отправляйте все запросы ip вашего сервера

Настройте .env файл

[ссылка на инструкцию](https://github.com/depocoder/star-burger/blob/main/README.md#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%82%D0%B5-%D0%B1%D1%8D%D0%BA%D0%B5%D0%BD%D0%B4)

Запустите контейнеры

```shell
docker-compose -f docker-compose.production.yml up -d
```

Установите nginx. [Ссылка на инструкцию](https://nginx.org/en/docs/install.html)

Создайте файл в `/etc/nginx/sites-enabled/star_burger`, с таким содержимым:

```nginx
server {
    listen 80 default;

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://web:8080/;
    }

    location /media/ {
        alias /media/;
    }

    location /static/ {
        alias /frontend/;
    }

} 
```

Создайте сертификаты. Скопируйте команду, указав свою почту и свой домен:

```shell
certbot --nginx --email ma1n.py@ya.ru --agree-tos --no-eff-email -d starburger.depocoder.xyz
```

Проведите миграции
```shell
docker exec star_burger_web "python" "manage.py" "migrate" "--no-input"
```

## Как быстро обновить код на сервере?
В репозитории есть заготовка для быстрого обновления кода.
```shell
./docker_deploy.sh
```

## Запуск тестов
```shell
docker exec star_burger_web "python" "manage.py" "test"
```

Теперь можете зайти адрес по домену на сервер у меня это  [https://starburger.depocoder.xyz/](https://starburger.depocoder.xyz/)

![](https://i.imgur.com/6eIGuKj.png)



