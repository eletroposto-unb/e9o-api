FROM python:3.10

WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "api.main:api", "--reload", "--port", "8080", "--host", "0.0.0.0"]