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
def test_list_organizations_with_term():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?term=affinity",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(term="affinity")
    assert "organizations" in result
    assert len(result["organizations"]) == 1
    assert result["organizations"][0]["name"] == "Affinity Inc"

@responses.activate
def test_search_organizations():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?term=example.com",
        json={"organizations": [{"id": 123, "name": "Example Corp", "domain": "example.com"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.search_organizations("example.com")
    assert "organizations" in result
    assert len(result["organizations"]) == 1
    assert result["organizations"][0]["id"] == 123
    assert result["organizations"][0]["name"] == "Example Corp"
    assert result["organizations"][0]["domain"] == "example.com"

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
