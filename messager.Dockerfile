FROM python:3.10

WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "messager.main:messager", "--reload", "--port", "8081", "--host", "0.0.0.0"]
