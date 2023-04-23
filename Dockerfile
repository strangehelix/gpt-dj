FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV GPTDJ_ENV=prod

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]