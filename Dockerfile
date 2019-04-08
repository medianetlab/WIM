FROM python:3.7.2

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn -b 0.0.0.0:8000 --access-logfile -", "wim.app:create_app()"]