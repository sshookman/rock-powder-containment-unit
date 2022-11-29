FROM skelebot/python-base
MAINTAINER Sean Shookman <sshookman@cars.com>
WORKDIR /app

RUN ["pip", "install", "numpy"]
RUN ["pip", "install", "pandas"]

COPY hello.py /app/hello.py

RUN apt-get update
RUN apt-get install -y git

CMD python hello.py
