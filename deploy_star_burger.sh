#!/bin/bash
set -e
echo 'load .env'
source .env
echo 'start git pull'
git pull
echo 'install py deps'
venv/bin/python3 -m pip install -r requirements.txt
echo 'install node deps'
npm install --also=dev
npm audit fix
echo 'run parcel build'
parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo 'run collectstatic'
venv/bin/python3 manage.py collectstatic --no-input
echo 'run migrate'
venv/bin/python3 manage.py migrate
echo 'run tests'
venv/bin/python3 manage.py test --keepdb
echo 'restart start-burger'
sudo systemctl restart star-burger.service

COMMIT_HAST=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d "{\"environment\": \"$ROLLBAR_ENVIRONMENT_NAME\", \"revision\": \"$COMMIT_HAST\"  , \"status\": \"succeeded\"}"
echo 'deploy completed'
