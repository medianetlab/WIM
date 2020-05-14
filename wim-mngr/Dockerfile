FROM python:3.7-slim

RUN mkdir -p /wim
WORKDIR /wim

COPY ./requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY ./wim /wim

CMD python ./wim-mngr.py