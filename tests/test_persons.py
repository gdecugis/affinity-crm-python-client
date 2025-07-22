import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_person():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons/123",
        json={"id": 123, "name": "John Doe"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_person(123)
    assert result["id"] == 123
    assert result["name"] == "John Doe"

@responses.activate
def test_get_person_with_opportunities():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons/123?with_opportunities=true",
        json={"id": 123, "name": "John Doe", "opportunities": [{"id": 1, "name": "Deal 1"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_person(123, with_opportunities=True)
    assert result["id"] == 123
    assert "opportunities" in result
    assert len(result["opportunities"]) == 1

@responses.activate
def test_get_person_with_multiple_params():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons/123?with_opportunities=true&with_interaction_dates=true&with_interaction_persons=true",
        json={"id": 123, "name": "John Doe", "opportunities": [], "interactions": [], "notes": []},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_person(123, with_opportunities=True, with_interaction_dates=True, with_interaction_persons=True)
    assert result["id"] == 123
    assert "opportunities" in result
    assert "interactions" in result or "notes" in result

@responses.activate
def test_list_persons():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons",
        json={"persons": [{"id": 1}, {"id": 2}], "next_page_token": "abc"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_persons()
    assert "persons" in result
    assert len(result["persons"]) == 2

@responses.activate
def test_list_persons_with_term():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons?page_size=50&term=doe",
        json={"persons": [{"id": 123, "name": "John Doe"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_persons(term="doe")
    assert "persons" in result
    assert len(result["persons"]) == 1
    assert result["persons"][0]["name"] == "John Doe"

@responses.activate
def test_list_persons_with_multiple_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons?page_size=50&term=doe&with_opportunities=true&with_interaction_dates=true",
        json={"persons": [{"id": 123, "name": "John Doe"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_persons(term="doe", with_opportunities=True, with_interaction_dates=True)
    assert "persons" in result
    assert len(result["persons"]) == 1

@responses.activate
def test_list_all_persons():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons",
        json={"persons": [{"id": 1}], "next_page_token": "next1"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons",
        json={"persons": [{"id": 2}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    results = list(client.list_all_persons())
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2