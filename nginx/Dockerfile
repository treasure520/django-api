FROM nginx:latest
LABEL maintainer="treasure.you@gmail.com"

COPY nginx.conf /etc/nginx/nginx.conf
COPY api-proxy.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled && \
    ln -s /etc/nginx/sites-available/api-proxy.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
