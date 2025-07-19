import responses
from affinity.client import AffinityClient

@responses.activate
def test_create_person():
    responses.add(
        responses.POST,
        "https://api.affinity.co/persons",
        json={"id": 321, "name": "New Person"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_person({"name": "New Person"})
    assert result["id"] == 321
    assert result["name"] == "New Person"

@responses.activate
def test_update_person():
    responses.add(
        responses.PATCH,
        "https://api.affinity.co/persons/321",
        json={"id": 321, "name": "Updated Person"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_person(321, {"name": "Updated Person"})
    assert result["id"] == 321
    assert result["name"] == "Updated Person"

@responses.activate
def test_delete_person():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/persons/321",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_person(321)
    assert result["deleted"] is True