FROM python:3.7-slim

RUN mkdir /wim-nbi
WORKDIR /wim-nbi

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["gunicorn -b 0.0.0.0:3000 --access-logfile -", "wim.app:create_app()"]