FROM python:3.7

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY prom-exporter/ /prom-exporter

CMD ["python", "/prom-exporter/exporter.py"]