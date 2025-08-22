import psutil
import socket
import requests
import json

BACKEND_URL = 'http://127.0.0.1:8000/receive/'
API_KEY = 'your-secret-api-key'

def collect_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'ppid']):
        try:
            info = proc.info
            memory_mb = info['memory_info'].rss / (1024 * 1024)  # Bytes to MB
            processes.append({
                'name': info['name'],
                'pid': info['pid'],
                'cpu_percent': info['cpu_percent'],
                'memory_mb': round(memory_mb, 2),
                'parent_pid': info['ppid'] if info['ppid'] != 0 else None
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return processes

def send_data():
    hostname = socket.gethostname()
    processes = collect_processes()
    data = {
        'hostname': hostname,
        'processes': processes
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': API_KEY
    }
    try:
        response = requests.post(BACKEND_URL, data=json.dumps(data), headers=headers)
        print(f'Status: {response.status_code}, Response: {response.text}')
    except Exception as e:
        print(f'Error sending data: {e}')

if __name__ == '__main__':
    send_data()