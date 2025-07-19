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
def test_get_organization_with_opportunities():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations/456?with_opportunities=true",
        json={
            "id": 456, 
            "name": "Serena Capital",
            "opportunity_ids": [123, 456],
            "opportunities": [
                {"id": 123, "name": "Series A"},
                {"id": 456, "name": "Series B"}
            ]
        },
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_organization(456, with_opportunities=True)
    assert result["id"] == 456
    assert result["name"] == "Serena Capital"
    assert "opportunity_ids" in result
    assert "opportunities" in result
    assert len(result["opportunities"]) == 2

@responses.activate
def test_get_organization_with_multiple_params():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations/456?with_opportunities=true&with_persons=true&with_notes=true",
        json={
            "id": 456, 
            "name": "Serena Capital",
            "opportunity_ids": [123],
            "opportunities": [{"id": 123, "name": "Series A"}],
            "person_ids": [789],
            "persons": [{"id": 789, "name": "John Doe"}],
            "notes": [{"id": 1, "content": "Test note"}]
        },
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_organization(456, with_opportunities=True, with_persons=True, with_notes=True)
    assert result["id"] == 456
    assert "opportunities" in result
    assert "persons" in result
    assert "notes" in result

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
        "https://api.affinity.co/organizations?page_size=50&term=affinity",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(term="affinity")
    assert "organizations" in result
    assert len(result["organizations"]) == 1
    assert result["organizations"][0]["name"] == "Affinity Inc"

@responses.activate
def test_list_organizations_with_list_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&list_id=456",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(list_id=456)
    assert "organizations" in result
    assert len(result["organizations"]) == 1

@responses.activate
def test_list_organizations_with_person_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&person_id=789",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(person_id=789)
    assert "organizations" in result
    assert len(result["organizations"]) == 1

@responses.activate
def test_list_organizations_with_opportunity_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&opportunity_id=101",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(opportunity_id=101)
    assert "organizations" in result
    assert len(result["organizations"]) == 1

@responses.activate
def test_list_organizations_with_multiple_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&list_id=456&person_id=789&term=affinity",
        json={"organizations": [{"id": 123, "name": "Affinity Inc"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_organizations(list_id=456, person_id=789, term="affinity")
    assert "organizations" in result
    assert len(result["organizations"]) == 1

@responses.activate
def test_search_organizations():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&term=example.com",
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
def test_search_organizations_with_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/organizations?page_size=50&term=example.com&list_id=456&person_id=789",
        json={"organizations": [{"id": 123, "name": "Example Corp", "domain": "example.com"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.search_organizations("example.com", list_id=456, person_id=789)
    assert "organizations" in result
    assert len(result["organizations"]) == 1
    assert result["organizations"][0]["id"] == 123

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
