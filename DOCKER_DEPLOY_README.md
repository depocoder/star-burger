# Инструкция по деплою на ваш сервер

Купите домен и отправляйте все запросы ip вашего сервера

## Настройте .env файл 

[ссылка на инструкцию](https://github.com/depocoder/star-burger/blob/main/README.md#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%82%D0%B5-%D0%B1%D1%8D%D0%BA%D0%B5%D0%BD%D0%B4)

## Запустите контейнеры
> При первом запуске будет build images
```shell
docker-compose -f docker-compose.production.yml up -d
```

## Войдите в nginx container
```
docker exec -it star_burger_nginx bash
```

## Создайте сертификаты
> Обратите внимание, что я указал свою почту и свой домен
> Сертификаты будут автоматически обновляться, после перезагрузки контейнера сертификаты останутся
```shell
certbot --nginx --email ma1n.py@ya.ru --agree-tos --no-eff-email -d starburger.depocoder.xyz
```

Можете выходить из container nginx

## Проведите миграции
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



