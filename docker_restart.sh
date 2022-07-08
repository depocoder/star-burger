#!/bin/bash
set -e
echo 'load .env'
source .env
echo 'start git pull'
git pull
echo 'build images'
docker-compose -f docker-compose.production.yml build web db
echo 'restart containers'
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml up -d
echo 'migrate'
docker exec star_burger_web "python" "manage.py" "migrate" "--no-input"
echo 'run tests'
docker exec star_burger_web "python" "manage.py" "test"
COMMIT_HAST=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d "{\"environment\": \"$ROLLBAR_ENVIRONMENT_NAME\", \"revision\": \"$COMMIT_HAST\"  , \"status\": \"succeeded\"}"
echo 'deploy completed'
