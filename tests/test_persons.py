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
        "https://api.affinity.co/persons?term=doe",
        json={"persons": [{"id": 123, "name": "John Doe"}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_persons(term="doe")
    assert "persons" in result
    assert len(result["persons"]) == 1
    assert result["persons"][0]["name"] == "John Doe"

@responses.activate
def test_search_persons():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons?term=john",
        json={"persons": [{"id": 123, "name": "John Doe", "email": "john@example.com"}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.search_persons("john")
    assert "persons" in result
    assert len(result["persons"]) == 1
    assert result["persons"][0]["id"] == 123
    assert result["persons"][0]["name"] == "John Doe"
    assert result["persons"][0]["email"] == "john@example.com"

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