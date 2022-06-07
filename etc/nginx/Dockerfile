FROM ubuntu:18.04

MAINTAINER Eranga Bandara (erangaeb@gmail.com)

# install nginx
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update -y
RUN apt-get install -y nginx

# install certbot
RUN add-apt-repository ppa:certbot/certbot
RUN apt-get update -y
RUN apt-get install -y certbot python-certbot-nginx
# deamon mode off
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx
RUN rm /etc/nginx/sites-enabled/default

# expose ports
EXPOSE 80 443

# add nginx staging conf
ADD etc/nginx/conf.d/local.conf /etc/nginx/sites-available/local.conf

# create symlinks
RUN ln -s /etc/nginx/sites-available/local.conf /etc/nginx/sites-enabled/local.conf

# work dir
WORKDIR /etc/nginx

# add entrypoing
ADD etc/nginx/docker-entrypoint.sh .

# make certs dir as volume
VOLUME ["/etc/letsencrypt"]

RUN chmod +x docker-entrypoint.sh

CMD ["/etc/nginx/docker-entrypoint.sh"]
