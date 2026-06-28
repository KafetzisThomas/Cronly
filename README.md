<div align="center">
    <h1>Cronly</h1>
    <p>A high-performance uptime monitoring tool.<br>Written in Python/Django</p>
</div>

## Features

- **Continuouss Monitoring:** Customizable URL ping intervals (minute to monthly).
- **Real-time Dashboard:** Live status (Up/Down) and RTT (min,max,avg) tracking.
- **Dynamic Scheduling:** Create, update or delete monitors.

## Database Schema

![Database Schema](assets/db_schema.png)

## Usage

### Local Development

First install `uv` and sync the project dependencies:

```bash
cd path/to/root/directory
pip install uv
uv sync
uv sync --extra dev  # for devs only
```

Migrate database:

```bash
uv run manage.py migrate
```

Start Redis server:

**Docker:** `docker run -d --name redis -p 6379:6379 redis`  
**Unix:** `sudo service redis-server start`

Run Django server via honcho (web server + celery worker + celery beat):

```bash
uv run honcho start
```

Access web application at `http://127.0.0.1:8000` or `http://localhost:8000`.
