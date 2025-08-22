import psutil
import socket
import requests
import json
import time
from datetime import datetime, timezone

BACKEND_URL = 'http://127.0.0.1:8000/receive/'
API_KEY = 'your-secret-api-key'

def collect_processes():
    processes = []

    # Prime CPU stats (first call always returns 0.0)
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except Exception:
            pass

    # short sleep to let psutil calculate CPU %
    time.sleep(0.2)

    for proc in psutil.process_iter(['pid', 'name', 'ppid']):
        try:
            with proc.oneshot():  # faster, reduces syscalls
                pid = proc.info['pid']
                name = proc.info.get('name') or ''
                ppid = proc.info.get('ppid')
                cpu = proc.cpu_percent(interval=None)   # now accurate
                mem_percent = proc.memory_percent()     # %
                mem_rss = proc.memory_info().rss        # bytes

                processes.append({
                    'pid': pid,
                    'ppid': ppid if ppid != 0 else None,
                    'name': name,
                    'cpu_percent': round(cpu, 2),
                    'mem_percent': round(mem_percent, 2),
                    'mem_rss': mem_rss,  # still include raw bytes if needed
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def send_data():
    hostname = socket.gethostname()
    processes = collect_processes()
    data = {
        'hostname': hostname,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'processes': processes
    }
    headers = {
        'X-API-KEY': API_KEY
    }
    try:
        response = requests.post(BACKEND_URL, json=data, headers=headers, timeout=15)
        print(f'Status: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'Error sending data: {e}')

if __name__ == '__main__':
    send_data()