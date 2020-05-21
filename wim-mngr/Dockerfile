FROM python:3.7-slim

RUN mkdir -p /wim-mngr
WORKDIR /wim-mngr

COPY ./requirements.txt .
RUN pip install --upgrade -r requirements.txt

COPY . /wim-mngr
ENV PYTHONPATH=/wim-mngr

CMD python ./wim/wim-mngr.py