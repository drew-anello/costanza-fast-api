FROM python:3.11-slim

WORKDIR /app/app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn

COPY . .

EXPOSE 80

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ['fastapi' 'run']