# AGENTS.md  
_Authoritative guide for all contributors to the **Mainframe Automation & Monitoring Portal** (Django 5.x)_

---

## 1  Overview

This project delivers a web‑based control plane for a z/OS 2.2 mainframe estate.  
Key goals:

* **Observability** – surfacing real‑time SMF/RMF metrics, job‑flow status, and alerting.  
* **Automation** – orchestrating routine mainframe tasks (IPL scheduling, JES3 queue hygiene, etc.) through REST and message queues.  
* **Reliability & Security** – every change is verified end‑to‑end before reaching production.

The repository uses:

| Layer | Technology |
|-------|------------|
| UI/API | Django 5.x + Django‑REST‑framework |
| Data   | PostgreSQL 16 |
| Async  | Celery 6 + Redis 7 (broker + result backend) |
| Container | Docker, deployed to Kubernetes/EKS (default) |
| Observability | Prometheus + Grafana, Sentry for tracing & error capture |

---

## 2  CI/CD Pipeline (GitHub Actions)

> File: **.github/workflows/ci‑cd.yml**




Security hardening – the pipeline uses GitHub OIDC rather than long‑lived AWS keys, eliminating secret sprawl. 
DevOpsCube

Observability integration – build & deploy steps emit release markers to Sentry via sentry-cli (omitted above for brevity). 
Sentry Docs

A nightly scheduled run executes dependency‑vulnerability scans (pip-audit) and server‑side “check --deploy” assertions.

Tip: Use reusable workflow call‑outs (workflow_call) if you maintain multiple repos.

3  Security Best Practices
Stay patched – subscribe to the Django security RSS feed; apply patch releases promptly (e.g., CVE‑2024‑56374 in Django 5.1.5). 
Django Project

Strict settings for production (DEBUG = False, ALLOWED_HOSTS, secure cookies, CSP headers).

OWASP checks – employ django‑secure‑checklist in the pipeline.

Static code + dependency analysis – Bandit, Safety/PyUp and pip-audit.

Secrets – only in GitHub Environments, AWS SSM, or Vault; never in git.

Database – use least‑privilege DB roles, run migrations in immutable transactions.

Authentication – SSO/OIDC against corporate IdP; MFA enforced.

Network – service mesh (mTLS) inside the cluster; expose ingress via WAF.

Refer to the official Django security guide for deeper rationale. 
Django Project
Django Project

4  Performance & Scalability Guidelines
Profiling first – establish baseline metrics (Pyroscope, django‑debug‑toolbar).

Database – optimise ORM usage (select_related, prefetch_related, explicit indexes). 
Django Project
gdtechblog.com

Caching – Redis for view‑level & low‑level caches; cache static fragments aggressively. 
Codez Up

Async – offload heavy workloads to Celery workers; use async views for I/O bound tasks. 
Codez Up

Horizontal scaling – each component is stateless; scale pods via HPA; migrations use “leader” init job.

Static assets – collected once into S3/CloudFront; immutable hashed filenames.

5  Monitoring & Observability
Metrics – django‑prometheus exposes default and custom app metrics scraped by Prometheus, visualised in Grafana dashboards. 
hodovi.cc
Highlight

Tracing & errors – Sentry SDK with sentry_sdk.integrations.django. 
Sentry Docs

Log aggregation – structured JSON logs to stdout ➜ Fluent Bit ➜ OpenSearch/Loki.

Synthetic probes – post‑deploy smoke tests executed by the pipeline (§2).

Alerting – Prometheus Alertmanager + PagerDuty escalation.

6  Coding Standards
Conform to PEP 8 and PEP 257 docstrings; enforced by Black, isort, flake8. 
Python Enhancement Proposals (PEPs)

Module/package naming follows PEP 423 recommendations. 
Python Enhancement Proposals (PEPs)

Limit cyclomatic complexity (radon cc) and maintain type hints (mypy --strict).

Every model/view/function must carry docstrings explaining intent, inputs, outputs.

7  Testing Strategy
Layer	Tool	Notes
Unit	pytest‑django	Fast, DB mocked by factories
Integration	pytest, Docker Compose	Runs against real Postgres + Redis
Contract	schemathesis	Ensures API schema stability
E2E	Playwright	Headless Chromium hitting k8s Ingress
Security	bandit, python‑safety	CVE scanning
Performance	Locust	Soak & load testing

Coverage threshold is ≥ 90 % lines, ≥ 80 % branches (§2).

8  Branching & PR Workflow
Fork ➜ feature branch (feat/<ticket‑id>-<slug>).

Commit in small, atomic units with Conventional Commits.

Open PR → CI runs (§2).

One approving review + green CI gates → auto‑merge (github.merge_queue).

Squash‑merge to keep history linear.

No direct pushes to main.

9  Documentation
MkDocs‑Material site (/docs) auto‑deployed to GitHub Pages on merge.

Architecture Decision Records (ADRs) under docs/adr/.

Each public API is documented in OpenAPI/Swagger; CI validates drift.

Docstrings are rendered into reference docs with mkdocstrings.

10  Local Development
bash
Copy
git clone <repo> && cd project
cp .env.example .env  # fill secrets
make dev              # starts Django + Postgres + Redis via docker‑compose
make lint test
Requires Docker 24+, Python 3.12 if running outside the compose network.

11  On‑Call & Runbook Highlights
Scenario	Playbook
PodCrashLoopBackOff	Check kubectl logs; redeploy if image pull error; verify Secrets.
High DB latency	SELECT * FROM pg_stat_activity to find slow query; review indexes.
Sentry spike	Inspect release diff, roll back via ArgoCD, tag incident‑<id>.

12  Extending the System
When adding a new feature:

Open an ADR draft.

Write failing tests first.

Implement code; run make format lint test.

Update docs + sample JSON payloads.

Raise PR ➜ CI passes ➜ review ➜ merge.

Remember: no test = no merge.

13  Credits & References
Django Security releases 
Django Project

GitHub Actions best‑practice CI/CD pipeline inspiration 
CodingEasyPeasy
GitHub

OIDC hardening for AWS deployments 
DevOpsCube

Prometheus + Grafana dashboards for Django 
hodovi.cc

PEP 8 & 423 Python conventions 
Python Enhancement Proposals (PEPs)
Python Enhancement Proposals (PEPs)

