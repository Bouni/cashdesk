FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /{app,data} && mkdir -p /app/templates
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY backend /app/

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
