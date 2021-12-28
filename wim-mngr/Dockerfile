FROM python:3.7

RUN mkdir -p /wim-mngr
RUN apt update && apt install curl -y
WORKDIR /wim-mngr

COPY ./requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY . /wim-mngr
ENV PYTHONPATH=/wim-mngr

CMD python ./wim/wim-mngr.py
