FROM python:3.11-alpine

RUN apk update \
    && apk upgrade \
    && apk add --no-cache build-base gcc python3-dev musl-dev mysql-client mysql-dev pkgconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

EXPOSE 5000

