# Selenium's official image ships Chrome + Chromedriver already wired up,
# which is the painful part of hosting Selenium. We add Python on top.
FROM selenium/standalone-chrome:127.0

USER root

# Install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

COPY . .

# Render provides $PORT; default to 8000 locally.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
