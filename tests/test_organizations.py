import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_organization():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations/456",
        json={"id": 456, "name": "Serena Capital"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_organization(456)
    assert result["id"] == 456
    assert result["name"] == "Serena Capital"

@responses.activate
def test_list_organizations():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations",
        json={"organizations": [{"id": 1}, {"id": 2}], "next_page_token": "abc"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations()
    assert "organizations" in result
    assert len(result["organizations"]) == 2

@responses.activate
def test_list_all_organizations():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations",
        json={"organizations": [{"id": 1}], "next_page_token": "next1"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations",
        json={"organizations": [{"id": 2}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    results = list(client.list_all_organizations())
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
