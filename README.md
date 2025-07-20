# AutoShift

AutoShift is a minimal Django-based project designed to demonstrate how to run
mainframe automation tasks, scrape hardware monitoring pages, and forward the
results to Splunk via the HTTP Event Collector (HEC).

## Features

- **Django** web interface with an asynchronous endpoint to trigger automation
  commands.
- **Mainframe automation stub** that can be extended to interact with z/OS or
  other mainframe environments.
- **System information collection** via `collect_system_info`.
- **Web scraping** using `httpx` and `BeautifulSoup` for monitoring pages.
- **Metrics parser** to extract key/value pairs from monitoring tables.
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
3. Run migrations and start the server (the application modules live under
   the `src/` directory):
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


### Deployment to OpenShift

The project ships with example manifests under `openshift/` for deploying the
container image to an OpenShift cluster.  A typical workflow is:

1. Build and push the image (the CI pipeline already does this):
   ```bash
   docker build -t ghcr.io/<your repo>/autoshift:latest .
   docker push ghcr.io/<your repo>/autoshift:latest
   ```
2. Log in to your OpenShift cluster and apply the resources:
   ```bash
   oc login https://api.cluster.example.com --token=<token>
   oc new-project autoshift || oc project autoshift
   oc apply -f openshift/
   ```

The `Route` resource exposes the Django service publicly. Update the
environment variables in `openshift/deployment.yaml` to match your Splunk HEC
endpoint and any production secrets.

