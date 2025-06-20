# Configurable Web Server

A lightweight, configurable HTTP server designed for testing and simulating various application behaviors in containerized environments. Perfect for testing service discovery, load balancers, and application startup scenarios.

## Features

- Configurable response content and HTTP status code
- Adjustable startup delay to simulate application initialization
- Configurable response delay to simulate processing time
- JSON responses with request metadata
- Graceful shutdown handling
- Detailed logging with timestamps
- Docker ready

## Quick Start

```bash
# Build the image
docker build -t configurable-server .

# Run with default settings
docker run -p 8080:8080 configurable-server

# Run with custom configuration
docker run -p 8080:8080 \
    -e SERVER_PORT=8080 \
    -e SERVER_RESPONSE="Custom Response" \
    -e STARTUP_DELAY=5 \
    -e RESPONSE_DELAY=2 \
    -e STATUS_CODE=503 \
    configurable-server
```

## Configuration

The server can be configured using environment variables:
Variable 	        Description 	                                Default 	        Example
SERVER_PORT 	    Port the server listens on 	                    8080 	            8080
SERVER_RESPONSE 	Custom response message 	                    "Hello World!" 	    "Custom Response"
STARTUP_DELAY 	    Delay in seconds before server starts 	            0 	             5
RESPONSE_DELAY 	    Delay in seconds before responding to each request 	0 	2
STATUS_CODE 	    HTTP status code to return 	                        200 	503


### Server Behavior
Startup Process

    Displays startup banner with timestamp
    Shows current configuration
    If STARTUP_DELAY > 0, shows countdown
    Indicates when server is ready to accept connections

Example startup output:
```bash
docker run -p 5678:5678     -e SERVER_PORT=5678     -e SERVER_RESPONSE="Custom Response"     -e STARTUP_DELAY=5     -e RESPONSE_DELAY=1     -e STATUS_CODE=200     configurable-server

==================================================
Starting Configurable Web Server at 2025-06-20 01:54:41 UTC
==================================================

Server Configuration:
--------------------
Port:           5678
Response:       Custom Response
Startup Delay:  5s
Response Delay: 1.0s
Status Code:    200

Server is listening on port 5678
Starting initialization phase...
Startup in progress... 5s remaining
Startup in progress... 4s remaining
Startup in progress... 3s remaining
Startup in progress... 2s remaining
Startup in progress... 1s remaining


Server is ready to accept connections at 2025-06-20 01:54:46 UTC
==================================================
```

### Request Handling

Each request is logged with timestamp
    Response includes:
        Custom message
        Status code
        Request path
        Configured response delay

### Example response:
```json

{
    "message": "Custom Response",
    "status": 503,
    "path": "/",
    "response_delay": 2.0
}
```

Example request log:
```bash
    
[2025-06-20 01:22:10 UTC] "GET / HTTP/1.1" 503 -
```

### Shutdown Process

    Captures SIGTERM and SIGINT signals
    Logs shutdown initiation with timestamp
    Performs graceful shutdown
    Indicates completion

Example shutdown output:
```bash
==================================================
Received shutdown signal: SIGINT at 2025-06-20 01:55:48 UTC
Starting graceful shutdown...
==================================================

Stopping HTTP server...
Server stopped successfully

Graceful shutdown completed

Shutting down server...
Server shutdown completed
```

### Use Cases

    Service Discovery Testing
        Simulate slow service startup
        Test service readiness detection

    Load Balancer Testing
        Configure different response times
        Test error handling with different status codes

    Application Behavior Simulation
        Simulate slow applications
        Test timeout handling
        Test error responses

    Container Orchestration Testing
        Test graceful shutdown handling
        Verify startup probe configurations
        Test service mesh behavior

### Testing Examples
Basic Test
```bash
while true; do curl -w "Status: %{http_code}, Time: %{time_total}s\n" -s localhost:5678; sleep 1; done
{"message": "Custom Response", "status": 200, "path": "/", "response_delay": 1.0}
Status: 200, Time: 1.002810s
{"message": "Custom Response", "status": 200, "path": "/", "response_delay": 1.0}
Status: 200, Time: 1.002633s
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
License

[MIT License](https://console.harmony.a2z.com/LICENSE)
