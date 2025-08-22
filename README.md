# System process monitoring

## Overview

This is a Django REST framework project for monitoring systems process

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Arvindsain/system_monitoring.git
cd system_monitoring
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r req.txt
```

### 5. Apply Migrations

```bash
cd process_monitor
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the Development Server

```bash
python manage.py runserver
```
### Create application
1. GO to monitor app in project 
2. Run 
```bash
pyinstaller --onefile agent.py
```
3. it will create agent.exe
4. Now double click it, it will send all processes data to backend.

### Process to get data and show in frontend

1. Copy agent to system from dist folder from monitor app.
2. Run agent by double clicking it.
3. It will send data to backend and save it in database.
4. Now open link below in browser
```bash
http://127.0.0.1:8000/static/index.html
```
5. In frontend you can see all the processes and hostname.