FROM python:3.7-slim

RUN mkdir -p /wim
WORKDIR /wim

COPY ./requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY . /wim
ENV PYTHONPATH=/wim

CMD python ./wim/wim-mngr.py