FROM python:3.11.10-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# คัดลอกไฟล์ในapp ไปยัง /code/app
COPY ./app /code/app

# app/main.py ต้องมี app เป็น FastAPI instance
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"] 