FROM python:3.9-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install required packages during build
RUN pip install requests

# Create a simple Python web server script
COPY /app/server.py /app/server.py

# Make the script executable
RUN chmod +x /app/server.py

# Set default environment variables for all possible ports
ENV SERVER_PORT_1=8080 \
    SERVER_RESPONSE_1="Hello from port 8080!" \
    STATUS_CODE_1=200 \
    RESPONSE_DELAY_1=0 \
    SERVER_PORT_2="" \
    SERVER_RESPONSE_2="" \
    STATUS_CODE_2="" \
    RESPONSE_DELAY_2="" \
    SERVER_PORT_3="" \
    SERVER_RESPONSE_3="" \
    STATUS_CODE_3="" \
    RESPONSE_DELAY_3="" \
    SERVER_PORT_4="" \
    SERVER_RESPONSE_4="" \
    STATUS_CODE_4="" \
    RESPONSE_DELAY_4="" \
    SERVER_PORT_5="" \
    SERVER_RESPONSE_5="" \
    STATUS_CODE_5="" \
    RESPONSE_DELAY_5="" \
    STARTUP_DELAY=0

# Expose all possible ports
EXPOSE 8080 8081 8082 8083 8084

CMD ["python", "-u", "/app/server.py"]

