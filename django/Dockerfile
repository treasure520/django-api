FROM python:latest
LABEL maintainer="treasure.you@gmail.com"

WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001
ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
CMD uwsgi --ini uwsgi.ini --static-map /static=./static
