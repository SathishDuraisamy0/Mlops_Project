FROM python:slim

ENV PYTHONDONTWRITECODE= 1 \
    PYTHONUNUNBUFFERD = 1 

WORKDIR /app

RUN apt-get update && apt -get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -e .

RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python","application.py"]

