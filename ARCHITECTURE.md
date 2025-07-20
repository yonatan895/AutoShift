# Architecture

This project demonstrates a lightweight approach to running automation commands
from a Django web interface and forwarding results to Splunk. The design favors
simplicity and security.

## Django Application

The `autoshift_core` app exposes a single asynchronous endpoint (`/core/run/`)
that accepts POST requests containing a `command`. The view executes this
command on the mainframe (via the placeholder in `mainframe.py`) and optionally
forwards the output to Splunk using `SplunkHECClient`.

- **Asynchronous View** – `run_automation` is declared with `async def`, allowing
the use of `await` for non-blocking HTTP requests when communicating with
Splunk.
- **CSRF Exemption** – Since automation may be triggered programmatically, CSRF
protection is disabled for this endpoint via `@csrf_exempt`. In a production
setup, alternative authentication (e.g., token-based) should be implemented.

## Splunk Integration

`autoshift_core/splunk.py` implements `SplunkHECClient`, wrapping the Splunk HTTP Event
Collector API using `httpx.AsyncClient`. Asynchronous I/O keeps request latency
low and the design ensures the Splunk endpoint and token are loaded from
environment variables, limiting risk of credential leakage.

## Web Scraping

`autoshift_core/scraper.py` uses `httpx` and `BeautifulSoup` to fetch and parse hardware
monitoring pages. `fetch_page_title` illustrates simple extraction while
`fetch_metrics` parses key/value tables from pages labelled with the `metrics`
CSS class.

## Mainframe Automation

`autoshift_core/mainframe.py` exposes `run_command` as a stub for executing
commands on a mainframe host. `collect_system_info` demonstrates how higher
level helpers can be composed on top of it. In real deployments this function
would interface with tools like `py3270` instead of subprocess calls.

## Testing Strategy

Unit tests under `autoshift_core/tests` rely on `httpx.MockTransport` to simulate network
interactions. This allows full test coverage without external dependencies. The
project uses `pytest` with the `asyncio` marker for async tests.

## Security Considerations

- Secrets (Django secret key and Splunk tokens) are loaded from environment
  variables.
- Only minimal code is executed on the server side; heavy automation should be
  delegated to worker processes for isolation.
- The example view is CSRF-exempt for demonstration purposes; production
  deployments should integrate proper authentication and authorization.

## Deployment

Container images are published to GitHub Container Registry by the CI pipeline.
The manifests under `openshift/` can be applied to any OpenShift cluster. A
`Route` object exposes the service externally while the `Deployment` runs the
Django process behind Gunicorn.

