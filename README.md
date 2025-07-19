# AutoShift

AutoShift is a minimal Django-based project designed to demonstrate how to run
mainframe automation tasks, scrape hardware monitoring pages, and forward the
results to Splunk via the HTTP Event Collector (HEC).

## Features

- **Django** web interface with an asynchronous endpoint to trigger automation
  commands.
- **Mainframe automation stub** that can be extended to interact with z/OS or
  other mainframe environments.
- **Web scraping** using `httpx` and `BeautifulSoup` for monitoring pages.
- **Splunk HEC client** for forwarding events.
- **Async architecture** for non-blocking I/O and better scalability.
- **Tests** written with `pytest` demonstrating usage of `httpx.MockTransport`.

## Requirements

- Python 3.8+
- See `requirements.txt` for Python dependencies.

## Usage

1. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
2. Set environment variables for Splunk and Django:
   ```bash
   export DJANGO_SECRET_KEY="replace-me"
   export SPLUNK_HEC_URL="https://splunk.example.com"
   export SPLUNK_HEC_TOKEN="your-token"
   ```
3. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
4. Send a POST request to `/core/run/` with a `command` parameter to execute an
   automation command.

## Running Tests

```bash
pytest
```

See `ARCHITECTURE.md` for additional details on project structure and advanced
features.

For mainframe data collection examples, see [docs/mainframe_to_splunk.md](docs/mainframe_to_splunk.md).
