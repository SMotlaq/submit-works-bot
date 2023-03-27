FROM python:3.9.7

COPY . .

RUN apt-get update && apt-get install -y tzdata

RUN pip install -r requirements.txt

WORKDIR /app

CMD ["python","main.py"]
