#!/bin/bash
set -e
echo 'load .env'
source .env
echo 'start git pull'
git pull
echo 'build images'
docker build frontend/ -t star_burger_frontend
docker-compose -f docker-compose.production.web.yml build web
echo 'run tests'
docker run star_burger_web python manage.py test
echo 'restart web'
docker-compose -f docker-compose.production.web.yml down
docker-compose -f docker-compose.production.web.yml up -d
echo 'migrate'
docker exec star_burger_web python manage.py migrate --no-input
echo 'copy static'
docker cp star_burger_web:/code/staticfiles/. ./static/
docker cp star_burger_frontend:/frontend/bundles/. ./static/

echo 'send deploy info to rollbar'
COMMIT_HAST=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d "{\"environment\": \"$ROLLBAR_ENVIRONMENT_NAME\", \"revision\": \"$COMMIT_HAST\"  , \"status\": \"succeeded\"}"
echo 'deploy completed'
