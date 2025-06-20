import http.server
import socketserver
import os
import time
import json
import sys
import signal
import datetime
import threading

# Configuration class for each port
class PortConfig:
    def __init__(self, port, response, status_code, response_delay):
        self.port = port
        self.response = response
        self.status_code = status_code
        self.response_delay = response_delay

# Global variables for server state
server_ready = False
startup_end_time = None
servers = []  # List to keep track of all server instances
server_threads = []  # List to keep track of all server threads

# Parse port configurations from environment variables
def get_port_configs():
    configs = []
    for i in range(1, 6):  # Support up to 5 ports
        port_env = os.getenv(f'SERVER_PORT_{i}')
        if port_env:
            configs.append(PortConfig(
                port=int(port_env),
                response=os.getenv(f'SERVER_RESPONSE_{i}', f'Hello from port {port_env}!'),
                status_code=int(os.getenv(f'STATUS_CODE_{i}', '200')),
                response_delay=float(os.getenv(f'RESPONSE_DELAY_{i}', '0'))
            ))
    return configs

# Get global configuration
STARTUP_DELAY = int(os.getenv('STARTUP_DELAY', '0'))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, port_config, **kwargs):
        self.port_config = port_config
        super().__init__(*args, **kwargs)

    def do_GET(self):
        global server_ready, startup_end_time
        
        if not server_ready:
            # Calculate remaining startup time
            if startup_end_time:
                remaining = max(0, int(startup_end_time - time.time()))
            else:
                remaining = 0
                
            # Return 503 during startup
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.send_header('Retry-After', str(remaining))
            self.end_headers()
            
            response_data = {
                'message': 'Server is starting up',
                'status': 503,
                'path': self.path,
                'port': self.port_config.port,
                'startup_remaining': remaining
            }
            self.wfile.write(json.dumps(response_data).encode() + b'\n')
            return

        # Normal request handling after startup
        time.sleep(self.port_config.response_delay)
        self.send_response(self.port_config.status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = {
            'message': self.port_config.response,
            'status': self.port_config.status_code,
            'path': self.path,
            'port': self.port_config.port,
            'response_delay': self.port_config.response_delay
        }
        
        self.wfile.write(json.dumps(response_data).encode() + b'\n')

    def log_message(self, format, *args):
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        sys.stderr.write(f"[{timestamp}] [Port {self.port_config.port}] {format%args}\n")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

def create_server(port_config):
    handler = lambda *args, **kwargs: CustomHandler(*args, port_config=port_config, **kwargs)
    return ThreadedHTTPServer(("", port_config.port), handler)

def run_server():
    global server_ready, startup_end_time, servers, server_threads
    
    # Get configurations for all ports
    port_configs = get_port_configs()
    if not port_configs:
        print("No port configurations found. Please set at least SERVER_PORT_1")
        sys.exit(1)

    start_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    print("\n" + "="*50)
    print(f"Starting Multi-Port Configurable Web Server at {start_time}")
    print("="*50)
    
    print("\nServer Configurations:")
    print("-"*20)
    for config in port_configs:
        print(f"\nPort {config.port}:")
        print(f"  Response:       {config.response}")
        print(f"  Status Code:    {config.status_code}")
        print(f"  Response Delay: {config.response_delay}s")
    print(f"\nStartup Delay:  {STARTUP_DELAY}s")
    sys.stdout.flush()

    if STARTUP_DELAY > 0:
        startup_end_time = time.time() + STARTUP_DELAY

    def signal_handler(signum, frame):
        signal_name = signal.Signals(signum).name
        shutdown_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f"\n{'='*50}")
        print(f"Received shutdown signal: {signal_name} at {shutdown_time}")
        print(f"Starting graceful shutdown...")
        print(f"{'='*50}")
        print(t("\nStopping HTTP servers..."))
        for server in servers:
            server.shutdown()
            server.server_close()
        print("All servers stopped successfully")
        print("\nGraceful shutdown completed")
        sys.stdout.flush()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Create and start all servers
        for config in port_configs:
            server = create_server(config)
            servers.append(server)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            server_threads.append(thread)
            thread.start()
            print(f"\nServer is listening on port {config.port}")

        print(f"Starting initialization phase...")
        sys.stdout.flush()

        if STARTUP_DELAY > 0:
            for i in range(STARTUP_DELAY, 0, -1):
                print(f"\rStartup in progress... {i}s remaining")
                sys.stdout.flush()
                time.sleep(1)
            print("\n")

        server_ready = True
        ready_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        print(f"All servers are ready to accept connections at {ready_time}")
        print("="*50 + "\n")
        sys.stdout.flush()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt...")
    except Exception as e:
        print(f"Error in server: {e}")
    finally:
        print("\nShutting down servers...")
        for server in servers:
            server.shutdown()
            server.server_close()
        # Wait for all threads to complete
        for thread in server_threads:
            thread.join(timeout=5)
        print("Server shutdown completed")
        sys.exit(0)

if __name__ == "__main__":
    run_server()

