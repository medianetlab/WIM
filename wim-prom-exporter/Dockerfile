FROM python:3.7

COPY . /prom_exporter
WORKDIR /prom_exporter

RUN pip install -r requirements.txt

ENV PYTHONPATH=/prom_exporter

CMD ["python", "prom_exporter/exporter.py"]