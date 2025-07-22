import responses
from affinity.client import AffinityClient

@responses.activate
def test_create_opportunity():
    responses.add(
        responses.POST,
        "https://api.affinity.co/opportunities",
        json={"id": 123, "name": "New Opportunity"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_opportunity(name="New Opportunity", list_id=1, organization_ids=None)
    assert result["id"] == 123
    assert result["name"] == "New Opportunity"

@responses.activate
def test_create_opportunity_with_organizations():
    responses.add(
        responses.POST,
        "https://api.affinity.co/opportunities",
        json={"id": 456, "name": "Opportunity with Orgs"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_opportunity(name="Opportunity with Orgs", list_id=1, organization_ids=[123, 456])
    assert result["id"] == 456
    assert result["name"] == "Opportunity with Orgs"

@responses.activate
def test_update_opportunity():
    responses.add(
        responses.PUT,
        "https://api.affinity.co/opportunities/123",
        json={"id": 123, "name": "Updated Opportunity"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_opportunity(123, name="Updated Opportunity")
    assert result["id"] == 123
    assert result["name"] == "Updated Opportunity"

@responses.activate
def test_delete_opportunity():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/opportunities/123",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_opportunity(123)
    assert result["deleted"] is True 