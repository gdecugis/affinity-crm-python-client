import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_person():
    responses.add(
        responses.GET,
        "https://api.affinity.co/persons/123",
        json={"id": 123, "name": "Guillaume"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_person(123)
    assert result["id"] == 123
    assert result["name"] == "Guillaume"

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