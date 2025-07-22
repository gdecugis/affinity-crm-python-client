import responses
from affinity.client import AffinityClient

@responses.activate
def test_list_fields():
    responses.add(
        responses.GET,
        "https://api.affinity.co/fields",
        json={"fields": [{"id": 1}, {"id": 2}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_fields()
    assert "fields" in result
    assert len(result["fields"]) == 2

@responses.activate
def test_list_fields_with_list_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/fields",
        json={"fields": [{"id": 1, "list_id": 123}, {"id": 2, "list_id": 123}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_fields(list_id=123)
    assert "fields" in result
    assert len(result["fields"]) == 2
    assert all(field.get("list_id") == 123 for field in result["fields"])

@responses.activate
def test_get_field():
    responses.add(
        responses.GET,
        "https://api.affinity.co/fields/42",
        json={"id": 42, "name": "Stage"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_field(42)
    assert result["id"] == 42
    assert result["name"] == "Stage"

@responses.activate
def test_list_field_values():
    responses.add(
        responses.GET,
        "https://api.affinity.co/field-values",
        json={"field_values": [{"id": 1, "value": "Active"}, {"id": 2, "value": "Inactive"}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_field_values(field_values_query_id=123)
    assert "field_values" in result
    assert len(result["field_values"]) == 2

@responses.activate
def test_list_field_values_with_field_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/field-values",
        json={"field_values": [{"id": 1, "value": "Active", "field_id": 42}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_field_values(field_values_query_id=123, field_id=42)
    assert "field_values" in result
    assert len(result["field_values"]) == 1
    assert result["field_values"][0]["field_id"] == 42