FROM ubuntu:18.04

# install nginx, certbot
RUN apt-get update -y &&  \
    apt-get install -y software-properties-common  \
    && add-apt-repository -y ppa:nginx/stable  \
    && apt-get update -y && \
    apt-get install -y nginx && \
    add-apt-repository ppa:certbot/certbot && \
    apt-get update -y && \
    apt-get install -y certbot python-certbot-nginx &&  \
    echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
    chown -R www-data:www-data /var/lib/nginx &&  \
    rm /etc/nginx/sites-enabled/default

# add nginx staging conf
ADD etc/nginx/conf.d/local.conf /etc/nginx/sites-available/local.conf

# create symlinks
RUN ln -s /etc/nginx/sites-available/local.conf /etc/nginx/sites-enabled/local.conf

# work dir
WORKDIR /etc/nginx

# add entrypoing
ADD etc/nginx/docker-entrypoint.sh .

RUN chmod +x docker-entrypoint.sh

CMD ["/etc/nginx/docker-entrypoint.sh"]
