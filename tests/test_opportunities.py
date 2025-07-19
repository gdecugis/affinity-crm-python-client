import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_opportunity():
    responses.add(
        responses.GET,
        "https://api.affinity.co/opportunities/789",
        json={"id": 789, "name": "Series A - Edgee"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_opportunity(789)
    assert result["id"] == 789
    assert result["name"] == "Series A - Edgee"

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
