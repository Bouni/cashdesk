FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ==============================================================================
# Install webserver and supervisor
RUN apt-get -y update && \
    apt-get install -y nginx supervisor 

RUN addgroup --system --gid 101 nginx && \
    adduser  --system --disabled-login --ingroup nginx --no-create-home --gecos "nginx user" --shell /bin/false --uid 101 nginx 
RUN mkdir /www /run/nginx && \
    chown -R nginx:nginx /var/lib/nginx  && \
    chown -R nginx:nginx /www

# ==============================================================================
# Install nodejs npm and yarn and build frontend
RUN apt-get install -y nodejs npm
RUN npm install -g npm@latest yarn @vue/cli

RUN mkdir /frontend
COPY frontend /frontend
RUN cd /frontend && yarn && yarn run build

# ==============================================================================
# setup backend and install its dependencies
RUN mkdir /{app,data} && mkdir -p /app/templates
WORKDIR /app

COPY backend/requirements.txt /app
RUN pip install -r requirements.txt

COPY backend /app/

# ==============================================================================
# Copy frontend files to the right places
RUN mkdir -p /app/static/{js,css}
RUN cp /frontend/dist/index.html /app/templates/ && \
    cp -r /frontend/dist/js /app/static/js/ && \
    cp -r /frontend/dist/css /app/static/css/

# ==============================================================================
# Setup webserver
COPY entrypoint.sh /entrypoint.sh 
COPY supervisord.conf /etc/supervisor/ 
COPY nginx.conf /etc/nginx/

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

