FROM python:3.12-slim

WORKDIR /promptlyBD

COPY ./requirements.txt /promptlyBD/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /promptlyBD/requirements.txt

COPY ./app /promptlyBD/app

COPY ./.env /promptlyBD/.env

COPY ./aipromptapp.db /promptlyBD/aipromptapp.db

CMD [ "fastapi", "run", "app/main.py", "--port", "80"]