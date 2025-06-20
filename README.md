# Multi-Port Echo Server

A configurable HTTP server that can listen on multiple ports simultaneously, with customizable responses, status codes, and delays for each port. Perfect for testing microservices, service discovery, and load balancer configurations.

## Features

- Support for up to 5 concurrent HTTP servers on different ports
- Individually configurable for each port:
  - Custom response messages
  - HTTP status codes
  - Response delays
- Configurable startup delay
- JSON responses with request metadata
- Detailed logging with timestamps
- Graceful shutdown handling
- Health check support
- Docker ready

## Quick Start

### Build the Image
```bash
docker build -t echo-server .


# Run with default settings
docker run -p 8080:8080 echo-server

# Run with custom configuration for multiple ports
docker run -p 8080:8080 -p 8081:8081 -p 8082:8082 \
    -e SERVER_PORT_1=8080 \
    -e SERVER_RESPONSE_1="Hello from port 8080" \
    -e STATUS_CODE_1=200 \
    -e RESPONSE_DELAY_1=0 \
    -e SERVER_PORT_2=8081 \
    -e SERVER_RESPONSE_2="Hello from port 8081" \
    -e STATUS_CODE_2=503 \
    -e RESPONSE_DELAY_2=2 \
    -e SERVER_PORT_3=8082 \
    -e SERVER_RESPONSE_3="Hello from port 8082" \
    -e STATUS_CODE_3=200 \
    -e RESPONSE_DELAY_3=1 \
    -e STARTUP_DELAY=10 \
    echo-server

```

## Configuration

The server can be configured using environment variables:
Variable 	        Description 	                                Default 	                    Example
SERVER_PORT_n 	        Port number for server n 	                    8080 (n=1) 	8081
SERVER_RESPONSE_n 	    Response message for port n 	               "Hello from port 8080!" (n=1) 	"Custom message"
STATUS_CODE_n 	        HTTP status code for port n 	                200 (n=1) 	                    503
RESPONSE_DELAY_n 	    Response delay in seconds for port n 	        0 (n=1) 	                    2

Global configuration:
Variable 	    Description 	                        Default 	Example
STARTUP_DELAY 	Initial delay before accepting requests 	0 	    10

### Server Behavior
Startup Process

    Displays startup banner with timestamp
    Shows current configuration
    If STARTUP_DELAY > 0, shows countdown
    Indicates when server is ready to accept connections

Example startup output:
```bash

docker run -p 8080:8080 -p 8081:8081 -p 8082:8082     -e SERVER_PORT_1=8080     -e SERVER_RESPONSE_1="Hello from port 8080"     -e STATUS_CODE_1=200     -e RESPONSE_DELAY_1=0     -e SERVER_PORT_2=8081     -e SERVER_RESPONSE_2="Hello from port 8081"     -e STATUS_CODE_2=503     -e RESPONSE_DELAY_2=2     -e SERVER_PORT_3=8082     -e SERVER_RESPONSE_3="Hello from port 8082"     -e STATUS_CODE_3=200     -e RESPONSE_DELAY_3=1     -e STARTUP_DELAY=10 echo-multiserver

==================================================
Starting Multi-Port Configurable Web Server at 2025-06-20 04:21:13 UTC
==================================================

Server Configurations:
--------------------

Port 8080:
  Response:       Hello from port 8080
  Status Code:    200
  Response Delay: 0.0s

Port 8081:
  Response:       Hello from port 8081
  Status Code:    503
  Response Delay: 2.0s

Port 8082:
  Response:       Hello from port 8082
  Status Code:    200
  Response Delay: 1.0s

Startup Delay:  10s

Server is listening on port 8080

Server is listening on port 8081

Server is listening on port 8082
Starting initialization phase...
Startup in progress... 10s remaining
Startup in progress... 9s remaining
Startup in progress... 8s remaining
Startup in progress... 7s remaining
Startup in progress... 6s remaining
Startup in progress... 5s remaining
Startup in progress... 4s remaining
Startup in progress... 3s remaining
Startup in progress... 2s remaining
Startup in progress... 1s remaining


All servers are ready to accept connections at 2025-06-20 04:21:23 UTC
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
  "message": "Hello from port 8080",
  "status": 200,
  "path": "/",
  "port": 8080,
  "response_delay": 0
}
```

```bash

[ec2-user@ip-172-31-38-100 ~]$ curl localhost:8080
{"message": "Hello from port 8080", "status": 200, "path": "/", "port": 8080, "response_delay": 0.0}
[ec2-user@ip-172-31-38-100 ~]$ curl localhost:8081
{"message": "Hello from port 8081", "status": 503, "path": "/", "port": 8081, "response_delay": 2.0}
[ec2-user@ip-172-31-38-100 ~]$ curl localhost:8082
{"message": "Hello from port 8082", "status": 200, "path": "/", "port": 8082, "response_delay": 1.0}
[ec2-user@ip-172-31-38-100 ~]$ curl localhost:8083
curl: (7) Failed to connect to localhost port 8083 after 0 ms: Couldn't connect to server
```

Example request log:
```bash
    
[2025-06-20 04:22:29 UTC] [Port 8080] "GET / HTTP/1.1" 200 -
[2025-06-20 04:22:36 UTC] [Port 8081] "GET / HTTP/1.1" 503 -
[2025-06-20 04:22:44 UTC] [Port 8082] "GET / HTTP/1.1" 200 -
```

### Shutdown Process

    Captures SIGTERM and SIGINT signals
    Logs shutdown initiation with timestamp
    Performs graceful shutdown
    Indicates completion

Example shutdown output:
```bash
==================================================
Received shutdown signal: SIGINT at 2025-06-20 04:23:48 UTC
Starting graceful shutdown...
==================================================
Error in server: name 't' is not defined

Shutting down servers...
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
while true; do 
    printf "Port 8080: "
    curl -w "Status: %{http_code}, Time: %{time_total}s\n" -s -o /dev/null localhost:8080
    printf "Port 8081: "
    curl -w "Status: %{http_code}, Time: %{time_total}s\n" -s -o /dev/null localhost:8081
    sleep 1
done

```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
License

[MIT License](https://console.harmony.a2z.com/LICENSE)
