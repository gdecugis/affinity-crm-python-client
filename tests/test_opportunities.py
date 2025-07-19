import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_opportunity():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities/456",
        json={"id": 456, "name": "Series A"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_opportunity(456)
    assert result["id"] == 456
    assert result["name"] == "Series A"

@responses.activate
def test_get_opportunity_with_interactions():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities/456?with_interactions=true",
        json={"id": 456, "name": "Series A", "interactions": [{"id": 1, "type": "email"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_opportunity(456, with_interactions=True)
    assert result["id"] == 456
    assert "interactions" in result
    assert len(result["interactions"]) == 1

@responses.activate
def test_get_opportunity_with_multiple_params():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities/456?with_interactions=true&with_notes=true&with_reminders=true",
        json={"id": 456, "name": "Series A", "interactions": [], "notes": [], "reminders": []},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_opportunity(456, with_interactions=True, with_notes=True, with_reminders=True)
    assert result["id"] == 456
    assert "interactions" in result
    assert "notes" in result
    assert "reminders" in result

@responses.activate
def test_list_opportunities():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities",
        json={"opportunities": [{"id": 1}, {"id": 2}], "next_page_token": "abc"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities()
    assert "opportunities" in result
    assert len(result["opportunities"]) == 2

@responses.activate
def test_list_opportunities_with_term():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&term=affinity",
        json={"opportunities": [{"id": 123, "name": "Affinity Investment"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities(term="affinity")
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1
    assert result["opportunities"][0]["name"] == "Affinity Investment"

@responses.activate
def test_list_opportunities_with_list_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&list_id=456",
        json={"opportunities": [{"id": 123, "name": "Affinity Investment"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities(list_id=456)
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1

@responses.activate
def test_list_opportunities_with_organization_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&organization_id=789",
        json={"opportunities": [{"id": 123, "name": "Affinity Investment"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities(organization_id=789)
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1

@responses.activate
def test_list_opportunities_with_person_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&person_id=101",
        json={"opportunities": [{"id": 123, "name": "Affinity Investment"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities(person_id=101)
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1

@responses.activate
def test_list_opportunities_with_multiple_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&list_id=456&organization_id=789&term=affinity",
        json={"opportunities": [{"id": 123, "name": "Affinity Investment"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_opportunities(list_id=456, organization_id=789, term="affinity")
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1

@responses.activate
def test_search_opportunities():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&term=series",
        json={"opportunities": [{"id": 456, "name": "Series A Investment", "stage": "Due Diligence"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.search_opportunities("series")
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1
    assert result["opportunities"][0]["id"] == 456
    assert result["opportunities"][0]["name"] == "Series A Investment"
    assert result["opportunities"][0]["stage"] == "Due Diligence"

@responses.activate
def test_search_opportunities_with_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities?page_size=50&term=series&list_id=456&organization_id=789",
        json={"opportunities": [{"id": 456, "name": "Series A Investment", "stage": "Due Diligence"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.search_opportunities("series", list_id=456, organization_id=789)
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1
    assert result["opportunities"][0]["id"] == 456

@responses.activate
def test_list_all_opportunities():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities",
        json={"opportunities": [{"id": 1}], "next_page_token": "next1"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities",
        json={"opportunities": [{"id": 2}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    results = list(client.list_all_opportunities())
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2
