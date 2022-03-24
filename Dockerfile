FROM python:3.9.7

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app

CMD ["python","main.py"]