FROM python:3.9
# I don't use 3.9-slim-buster
# because slim-buster hasn't had python3-dev and other debs for postgres engine

ENV POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY src/ /code

CMD ["python", "-m", "gunicorn", "-b", "127.0.0.1:8080", "star_burger.wsgi:application"]
