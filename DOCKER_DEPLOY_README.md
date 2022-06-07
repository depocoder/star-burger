# Инструкция по деплою на ваш сервер

Купите домен и отправляйте все запросы ip вашего сервера

## Сборка nginx docker
```shell
docker build -f etc/nginx/Dockerfile -t depocoder/nginx_certbot:0.1 .
```

## Запустите nginx docker

## Войдите в nginx container
docker exec -it nginx bash

## Создайте сертификаты
> Обратите внимание, что я указал свою почту и свой домен
> Сертификаты будут автоматически обновляться, после перезагрузки контейнера сертификаты останутся
```shell
certbot --nginx --email ma1n.py@ya.ru --agree-tos --no-eff-email -d starburger.depocoder.xyz
```

Можете выходить из container nginx

Проведите миграции
```shell
docker exec star_burger_web "python" "manage.py" "migrate" "--no-input"
```

Теперь можете зайти адрес по домену на сервер у меня это  [https://starburger.depocoder.xyz/](https://starburger.depocoder.xyz/)

![](https://i.imgur.com/6eIGuKj.png)

