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

## Methods

### Lists
```python
client.list_lists()
client.get_list(list_id: int)
client.create_list(name: str, type: int, is_public: bool, owner_id: Optional[int] = None, additional_permissions: Optional[list] = None)
```

### List Entries
```python
client.list_list_entries(list_id: int, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.get_list_entry(entry_id: int)
client.add_list_entry(list_id: int, entity_id: int, creator_id: Optional[int] = None)
client.delete_list_entry(list_id: int, list_entry_id: int)
client.list_all_list_entries(list_id: int, page_size: int = 50)
```

### Fields
```python
client.list_fields(list_id: Optional[int] = None, value_type: Optional[int] = None, entity_type: Optional[int] = None, with_modified_names: Optional[bool] = None, exclude_dropdown_options: Optional[bool] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.get_field(field_id: int)
client.create_field(name: str, entity_type: int, value_type: int, list_id: Optional[int] = None, allows_multiple: Optional[bool] = None, is_list_specific: Optional[bool] = None, is_required: Optional[bool] = None)
client.delete_field(field_id: int)
```

### Field Values
```python
client.list_field_values(field_values_query_id: int, entity_type: Optional[int] = None, field_id: Optional[int] = None, page_size: Optional[int] = None, page_token: Optional[str] = None)
client.list_field_value_changes(field_id: int, field_value_changes_query_id: int, entity_type: Optional[int] = None, action_type: Optional[int] = None)
client.create_field_value(field_id: int, value: Union[str, int, float, bool, list, dict], entity_id: int, list_entry_id: Optional[int] = None)
client.update_field_value(field_value_id: int, value: Union[str, int, float, bool, list, dict])
client.delete_field_value(field_value_id: int)
client.set_field_value(field_id: int, value: Union[str, int, float, bool, list, dict], entity_id: int, entity_type: Optional[int] = None, list_entry_id: Optional[int] = None)
```

### Persons
```python
client.list_persons(term: Optional[str] = None, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, with_current_organizations: Optional[bool] = None, min_interaction_date: Optional[str] = None, max_interaction_date: Optional[str] = None, page_size: int = 50, page_token: Optional[str] = None)
client.get_person(person_id: int, with_interaction_dates: Optional[bool] = None, with_interaction_persons: Optional[bool] = None, with_opportunities: Optional[bool] = None, with_current_organizations: Optional[bool] = None)
client.create_person(first_name: str, last_name: str, emails: List[str], organization_ids: Optional[List[int]] = None)
client.update_person(person_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, emails: Optional[List[str]] = None, organization_ids: Optional[List[int]] = None)
client.delete_person(person_id: int)
client.list_all_persons(page_size: int = 50)
```

### Organizations
```python
client.list_organizations(term: Optional[str] = None, page_size: int = 50, page_token: Optional[str] = None, list_id: Optional[int] = None, person_id: Optional[int] = None, opportunity_id: Optional[int] = None)
client.get_organization(org_id: int, with_opportunities: Optional[bool] = None, with_persons: Optional[bool] = None, with_interactions: Optional[bool] = None, with_notes: Optional[bool] = None, with_reminders: Optional[bool] = None, with_files: Optional[bool] = None)
client.create_organization(name: str, domain: Optional[str] = None)
client.update_organization(org_id: int, name: Optional[str] = None, domain: Optional[str] = None)
client.delete_organization(org_id: int)
client.list_all_organizations(page_size: int = 50)
```

### Opportunities
```python
client.list_opportunities(page_size: int = 50, page_token: Optional[str] = None, term: Optional[str] = None, list_id: Optional[int] = None, organization_id: Optional[int] = None, person_id: Optional[int] = None)
client.get_opportunity(opp_id: int, with_interactions: Optional[bool] = None, with_notes: Optional[bool] = None, with_reminders: Optional[bool] = None, with_files: Optional[bool] = None)
client.create_opportunity(name: str, list_id: int, organization_ids: Optional[List[int]] = None)
client.update_opportunity(opp_id: int, name: Optional[str] = None)
client.delete_opportunity(opp_id: int)
client.list_all_opportunities(page_size: int = 50)
```

### Notes
```python
client.list_notes(entity_id: int, entity_type: str)
client.create_note(note: str, creator_id: int, entity_id: int, entity_type: str)
client.update_note(note_id: int, note: Optional[str] = None)
client.delete_note(note_id: int)
```

### Interactions
```python
client.list_interactions(person_id: Optional[int] = None, organization_id: Optional[int] = None, opportunity_id: Optional[int] = None, list_entry_id: Optional[int] = None)
client.get_interaction(interaction_id: int, type: str)
client.create_interaction(interaction_type: str, subject: str, date: str, creator_id: int, participants: list, entity_id: int, entity_type: str, notes: Optional[str] = None)
client.update_interaction(interaction_id: int, interaction_type: Optional[str] = None, subject: Optional[str] = None, date: Optional[str] = None, creator_id: Optional[int] = None, participants: Optional[list] = None, entity_id: Optional[int] = None, entity_type: Optional[str] = None, notes: Optional[str] = None)
client.delete_interaction(interaction_id: int)
```

### Webhooks
```python
client.get_webhook(webhook_subscription_id: Optional[str] = None)
client.create_webhook(url: str, event: str)
client.update_webhook(webhook_subscription_id: str, url: Optional[str] = None, event: Optional[str] = None)
client.delete_webhook(webhook_subscription_id: str)
```

### Utility
```python
client.whoami()
client.get_rate_limit_status()
client.get_relationship_strengths(external_id: int)
```

---

## Entity Type Codes

For field values operations, use these entity type codes:
- `0` = Person
- `1` = Organization  
- `8` = Opportunity
- `list_entry_id` = List Entry (no numeric code)

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
✅ Robust entity type detection for field values  
📦 PyPI release ready

---

## Disclaimer

This is an unofficial client. Affinity is a trademark of Affinity, Inc. This project is maintained independently.