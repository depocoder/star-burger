FROM python:3.9

ENV POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY . /code

CMD ["python", "-m", "gunicorn", "-b", "127.0.0.1:8080", "star_burger.wsgi:application"]
