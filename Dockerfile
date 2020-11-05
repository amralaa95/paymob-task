FROM python:3.6-alpine3.9

#Installing essential packages
EXPOSE 8000

WORKDIR /paymob_task/
RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    && apk add linux-headers python3-dev libxslt-dev libxml2-dev mysql-dev gcc musl-dev jpeg-dev zlib-dev mysql-client g++ \
    && apk add ca-certificates wget

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN apk del .build-deps

ADD . .

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD ["./run.sh web"]