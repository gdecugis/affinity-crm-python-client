import responses
from affinity.client import AffinityClient

@responses.activate
def test_add_list_entry():
    responses.add(
        responses.POST,
        "https://api.affinity.co/lists/789/list-entries",
        json={"id": 456, "entity_id": 123, "entity_type": "person"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.add_list_entry(789, 123)
    assert result["id"] == 456
    assert result["entity_id"] == 123
    assert result["entity_type"] == "person"

@responses.activate
def test_delete_list_entry():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/lists/789/list-entries/456",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_list_entry(789, 456)
    assert result["deleted"] is True

 