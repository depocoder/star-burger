#!/bin/bash
set -e
echo 'load .env'
source .env
echo 'start git pull'
git pull
echo 'install py deps'
poetry install
echo 'install node deps'
npm install --also=dev
npm audit fix
echo 'run parcel build'
parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo 'run collectstatic'
poetry run python manage.py collectstatic --no-input
echo 'run migrate'
poetry run python manage.py migrate  --no-input
echo 'run tests'
poetry run python manage.py test --keepdb
echo 'restart start-burger'
sudo systemctl restart star-burger.service

COMMIT_HAST=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d "{\"environment\": \"$ROLLBAR_ENVIRONMENT_NAME\", \"revision\": \"$COMMIT_HAST\"  , \"status\": \"succeeded\"}"
echo 'deploy completed'
