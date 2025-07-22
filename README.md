# Affinity CRM Python Client

Unofficial Python client for the [Affinity CRM API (v1)](https://api-docs.affinity.co/#introduction).

This library supports both read and write operations for the Affinity v1 API, including:
- Persons (read & write)
- Organizations (read & write)
- Opportunities (read & write)
- Lists & List Entries (read & write)
- Fields & Field Values (read & write)
- Notes (read & write)
- Interactions (read & write)
- Webhooks (read & write)
- Relationship strengths & rate limits

Pagination is handled via both manual (`page_token`) and auto-paginated generators (`list_all_*`).

All API parameters are validated using Pydantic models, ensuring type safety and clear error messages.

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
new_org = client.create_organization(
    name="Example Corp",
    domain="example.com"
)

# Create an opportunity with custom fields
opportunity = client.create_opportunity(
    name="Deal with Example Corp",
    organization_ids=[new_org["id"]],
    list_id=12345
)

# Set custom field values (smart method that creates or updates)
client.set_field_value(
    field_id=123,
    value="Active",
    entity_id=opportunity["id"],
    list_entry_id=opportunity["list_entries"][0]["id"]
)

# List field values for an entity
field_values = client.list_field_values(
    field_values_query_id=opportunity["id"],
    field_id=123
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
✅ Write (POST, PUT, DELETE) support implemented  
✅ Field value creation and updates  
✅ Pydantic validation for all parameters  
✅ Smart field value management (`set_field_value`)  
✅ Auto-pagination generators (`list_all_*`)  
📦 PyPI release ready

---

## Disclaimer

This is an unofficial client. Affinity is a trademark of Affinity, Inc. This project is maintained independently.