FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN adduser --disabled-password django-user

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app

RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    /env/bin/pip install -r /tmp/requirements.txt

ENV PATH="/env/bin:$PATH"

USER django-user
