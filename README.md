# Affinity CRM Python Client

Unofficial Python client for the [Affinity CRM API (v1)](https://api-docs.affinity.co/#introduction).

This library supports both read and write operations for the Affinity v1 API, including:
- Persons (read & write)
- Organizations (read & write)
- Opportunities (read & write)
- Lists & List Entries (read & write)
- Fields & Field Values (read & write)
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

# Create an organization
org_data = {
    "name": "Example Corp",
    "domain": "example.com"
}
new_org = client.create_organization(org_data)

# Create an opportunity with custom fields
opportunity_data = {
    "name": "Deal with Example Corp",
    "organization_ids": [new_org["id"]],
    "list_id": 12345
}
opportunity = client.create_opportunity(opportunity_data)

# Set custom field values
client.set_field_value(
    field_id=123,
    value="Active",
    entity_id=opportunity["id"],
    list_entry_id=opportunity["list_entries"][0]["id"]
)
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
✅ Write (POST, PATCH, DELETE) support implemented  
✅ Field value creation and updates  
📦 PyPI release ready

---

## Disclaimer

This is an unofficial client. Affinity is a trademark of Affinity, Inc. This project is maintained independently.