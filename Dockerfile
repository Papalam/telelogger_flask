FROM python:3.10-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app/ /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "wsgi:app" ]