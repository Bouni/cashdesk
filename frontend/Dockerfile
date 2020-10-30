# dev stage
FROM node:buster-slim as dev-stage
WORKDIR /app
COPY frontend/package*.json /app/
RUN npm install -timeout=9999999

# build stage
FROM dev-stage as build-stage
COPY frontend /app/
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist/ /app
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
