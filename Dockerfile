FROM python:3.5-slim

MAINTAINER akalamoyo@gmail.com

USER root

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

EXPOSE 80

ENV NAME World

CMD ["python", "app.py"]
