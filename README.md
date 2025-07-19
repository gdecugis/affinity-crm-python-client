# Affinity CRM Python Client

Unofficial Python client for the [Affinity CRM API (v1)](https://api-docs.affinity.co/#introduction).

This library supports all read-only endpoints of the Affinity v1 API, including:
- Persons
- Organizations
- Opportunities
- Lists & List Entries
- Fields
- Relationship strengths & rate limits

Pagination is handled via both manual (`page_token`) and auto-paginated generators (`list_all_*`).

---

## Installation

```bash
pip install -e .[dev]
```

---

## Usage

```python
from affinity.client import AffinityClient

client = AffinityClient(api_key="your_api_key")

# Get a person by ID
person = client.get_person(123)

# List all organizations (auto-paginated)
for org in client.list_all_organizations():
    print(org["name"])

# Get current API user
print(client.whoami())
```

---

## Development & Testing

```bash
pytest
```

Tests use `responses` to mock API calls, so no real Affinity data is accessed.

---

## License

MIT — see `LICENSE` file.

---

## Status

✅ Read endpoints implemented and tested  
🚧 Write (POST, PATCH, DELETE) support planned  
📦 PyPI release TBD

---

## Disclaimer

This is an unofficial client. Affinity is a trademark of Affinity, Inc. This project is maintained independently.