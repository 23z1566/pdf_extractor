FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# This will run your script automatically
CMD ["python", "extractor1B.py"]
