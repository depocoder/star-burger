FROM nginx:stable

# install certbot
RUN add-apt-repository ppa:certbot/certbot && apt-get update -y && apt-get install -y certbot python-certbot-nginx

# deamon mode off
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

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

CMD ["/etc/nginx/docker-entrypoint.sh"]