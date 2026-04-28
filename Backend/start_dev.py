import subprocess
import time
import os
import signal
import webbrowser
from typing import List

# --- Configuration ---
FASTAPI_PORT = 8000
FRONTEND_PORT = 5173
FRONTEND_URL = f"http://localhost:{FRONTEND_PORT}"

# Commands to run each service.
# The `uvicorn` and `celery` commands must be run from the root directory.
# `npm run dev` must be run from the directory containing package.json (assumed to be the current directory).
SERVICE_COMMANDS = [
    # 1. FastAPI Backend API
    # Runs the app on port 8000 with auto-reload for development
    {
        "name": "FastAPI Backend",
        "command": ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", str(FASTAPI_PORT), "--reload"],
        "ready_message": f"Uvicorn running on http://127.0.0.1:{FASTAPI_PORT}",
        "log_color": "\033[94m" # Blue
    },
    # 2. Celery Worker
    # Must be run *after* Redis and the app are available.
    {
        "name": "Celery Worker",
        "command": ["celery", "-A", "worker", "worker", "-l", "info", "-c", "1"],
        "ready_message": "broker_connection_established",
        "log_color": "\033[92m" # Green
    },
    # 3. React Frontend (Vite)
    {
        "name": "Vite Frontend",
        "command": ["npm", "run", "dev"],
        "ready_message": f"Local: {FRONTEND_URL}",
        "log_color": "\033[93m" # Yellow
    }
]

# --- Helper Functions ---

def run_services():
    """Starts all services concurrently."""
    processes: List[subprocess.Popen] = []

    print("-" * 50)
    print(f"Starting Integrated Smart Farming Stack...")
    print("-" * 50)
    print(f"Frontend URL: {FRONTEND_URL}\n")
    print(f"NOTE: Ensure Redis is running before starting the Celery worker.")

    # Start all processes
    for service in SERVICE_COMMANDS:
        try:
            # Popen starts the process in the background
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            processes.append(process)
            print(f"{service['log_color']}>> Starting {service['name']} (PID: {process.pid}) ...\033[0m")
        except FileNotFoundError:
            print(f"\033[91mERROR: Command not found for {service['name']}. Is it installed? Command: {' '.join(service['command'])}\033[0m")
            return

    # Wait for the servers to start
    print("\nWaiting for services to become ready (up to 10 seconds)...")
    time.sleep(5) # Give initial processes time to spin up

    # 4. Open Browser
    print(f"\n\033[95mOpening frontend in browser: {FRONTEND_URL}\033[0m")
    webbrowser.open_new_tab(FRONTEND_URL)

    # 5. Continuous logging and signal handling
    def signal_handler(sig, frame):
        """Gracefully terminates all child processes."""
        print("\n\n\033[91m[STOPPING] Received termination signal. Shutting down all services...\033[0m")
        for p in processes:
            if p.poll() is None: # Only kill if still running
                try:
                    # Send SIGINT (Ctrl+C equivalent) for graceful shutdown
                    p.terminate()
                except Exception as e:
                    print(f"Could not terminate process {p.pid}: {e}")
        
        # Give a moment for processes to clean up
        time.sleep(2)
        
        # Kill any processes that didn't terminate
        for p in processes:
            if p.poll() is None:
                p.kill()
        
        print("\n\033[92mAll services stopped. Exiting.\033[0m")
        exit(0)

    # Register the signal handlers for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("\n--- Service Logs (Press Ctrl+C to Stop) ---")
    
    # Simple loop to keep the script running and check process status
    try:
        while True:
            # Check for termination of any process
            for i, p in enumerate(processes):
                # Poll checks if the process is still running
                if p.poll() is not None:
                    # If any service fails, stop the orchestrator
                    print(f"\n\033[91m[CRITICAL] {SERVICE_COMMANDS[i]['name']} (PID: {p.pid}) failed with exit code {p.returncode}. Stopping all services.\033[0m")
                    signal_handler(None, None) # Trigger clean shutdown
                    return

            time.sleep(1) # Wait 1 second before checking again
    except KeyboardInterrupt:
        # Handled by the signal_handler
        signal_handler(None, None)


if __name__ == '__main__':
    # Add project root directory to PATH for shell commands to work easily
    os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + os.pathsep + os.environ['PATH']
    run_services()