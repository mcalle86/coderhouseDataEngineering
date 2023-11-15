FROM python:3.10-slim

RUN mkdir /app
WORKDIR /app
COPY . /app
ENV SIZER 4
RUN apt-get update && apt-get install -y libpq-dev build-essential && apt autoremove && apt clean
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3","-u","main.py"]