FROM python:3.8.5-alpine
RUN pip install --upgrade pip
COPY . /interns-starter-flask-app
WORKDIR /interns-starter-flask-app/src
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN pip install -r ../requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]