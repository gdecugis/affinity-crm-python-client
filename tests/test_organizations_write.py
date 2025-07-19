import responses
from affinity.client import AffinityClient

@responses.activate
def test_create_organization():
    responses.add(
        responses.POST,
        "https://api.affinity.co/organizations",
        json={"id": 789, "name": "New Organization"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_organization({"name": "New Organization"})
    assert result["id"] == 789
    assert result["name"] == "New Organization"

@responses.activate
def test_update_organization():
    responses.add(
        responses.PATCH,
        "https://api.affinity.co/organizations/789",
        json={"id": 789, "name": "Updated Organization"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_organization(789, {"name": "Updated Organization"})
    assert result["id"] == 789
    assert result["name"] == "Updated Organization"

@responses.activate
def test_delete_organization():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/organizations/789",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_organization(789)
    assert result["deleted"] is True 