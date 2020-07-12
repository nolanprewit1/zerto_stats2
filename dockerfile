FROM alpine:latest
RUN apk add python3
RUN apk add py3-pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
ENTRYPOINT ["python3"]
CMD ["run.py"]