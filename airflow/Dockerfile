FROM apache/airflow:2.7.2

USER root
RUN apt-get update && apt autoremove && apt clean
USER airflow

ENV PYTHONPATH "${PYTHONPATH}:/opt/airflow"
COPY requirements.txt .
COPY .env /opt/airflow/

RUN pip install --user -r requirements.txt

#COPY . .
