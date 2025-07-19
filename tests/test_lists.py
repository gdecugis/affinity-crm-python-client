import responses
from affinity.client import AffinityClient

@responses.activate
def test_get_list():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101",
        json={"id": 101, "name": "VC Targets"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_list(101)
    assert result["id"] == 101
    assert result["name"] == "VC Targets"

@responses.activate
def test_list_lists():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists",
        json={"lists": [{"id": 1}, {"id": 2}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_lists()
    assert "lists" in result
    assert len(result["lists"]) == 2

@responses.activate
def test_get_list_entry():
    responses.add(
        responses.GET,
        "https://api.affinity.co/list-entries/555",
        json={"id": 555, "entity_id": 999},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_list_entry(555)
    assert result["id"] == 555
    assert result["entity_id"] == 999

@responses.activate
def test_list_list_entries():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries",
        json={"list_entries": [{"id": 1}, {"id": 2}], "next_page_token": "abc"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_list_entries(101)
    assert "list_entries" in result
    assert len(result["list_entries"]) == 2

@responses.activate
def test_list_list_entries_with_person_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries?page_size=50&person_id=789",
        json={"list_entries": [{"id": 1, "entity_id": 789}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_list_entries(101, person_id=789)
    assert "list_entries" in result
    assert len(result["list_entries"]) == 1
    assert result["list_entries"][0]["entity_id"] == 789

@responses.activate
def test_list_list_entries_with_organization_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries?page_size=50&organization_id=456",
        json={"list_entries": [{"id": 1, "entity_id": 456}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_list_entries(101, organization_id=456)
    assert "list_entries" in result
    assert len(result["list_entries"]) == 1
    assert result["list_entries"][0]["entity_id"] == 456

@responses.activate
def test_list_list_entries_with_opportunity_id():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries?page_size=50&opportunity_id=123",
        json={"list_entries": [{"id": 1, "entity_id": 123}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_list_entries(101, opportunity_id=123)
    assert "list_entries" in result
    assert len(result["list_entries"]) == 1
    assert result["list_entries"][0]["entity_id"] == 123

@responses.activate
def test_list_list_entries_with_multiple_filters():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries?page_size=50&person_id=789&organization_id=456",
        json={"list_entries": [{"id": 1, "entity_id": 789}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.list_list_entries(101, person_id=789, organization_id=456)
    assert "list_entries" in result
    assert len(result["list_entries"]) == 1

@responses.activate
def test_list_all_list_entries():
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries",
        json={"list_entries": [{"id": 1}], "next_page_token": "next1"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://api.affinity.co/lists/101/list-entries",
        json={"list_entries": [{"id": 2}], "next_page_token": None},
        status=200,
    )
    client = AffinityClient(api_key="test")
    results = list(client.list_all_list_entries(101))
    assert len(results) == 2
    assert results[0]["id"] == 1
    assert results[1]["id"] == 2