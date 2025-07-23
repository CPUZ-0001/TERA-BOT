FROM python:3.11-slim

RUN apt-get update && apt-get install -y aria2

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]
