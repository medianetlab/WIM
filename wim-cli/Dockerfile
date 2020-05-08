FROM python:3.7-slim

RUN mkdir /wim-cli
WORKDIR /wim-cli

COPY . .

RUN pip install .

CMD /bin/bash