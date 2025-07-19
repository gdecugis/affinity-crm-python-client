import responses
from affinity.client import AffinityClient

@responses.activate
def test_list_fields():
    responses.add(
        responses.GET,
        "https://api.affinity.co/fields",
        json={"fields": [{"id": 1}, {"id": 2}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_fields()
    assert "fields" in result
    assert len(result["fields"]) == 2

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