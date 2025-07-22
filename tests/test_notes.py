import responses
from affinity.client import AffinityClient

@responses.activate
def test_list_notes():
    responses.add(
        responses.GET,
        "https://api.affinity.co/notes",
        json={"notes": [{"id": 1, "note": "Test note"}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_notes(entity_id=123, entity_type="organization")
    assert "notes" in result
    assert len(result["notes"]) == 1
    assert result["notes"][0]["note"] == "Test note"

@responses.activate
def test_create_note():
    responses.add(
        responses.POST,
        "https://api.affinity.co/notes",
        json={"id": 2, "note": "Created note"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_note(note="Created note", creator_id=1, entity_id=123, entity_type="organization")
    assert result["id"] == 2
    assert result["note"] == "Created note"

@responses.activate
def test_update_note():
    responses.add(
        responses.PUT,
        "https://api.affinity.co/notes/2",
        json={"id": 2, "note": "Updated note"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_note(2, note="Updated note")
    assert result["id"] == 2
    assert result["note"] == "Updated note"

@responses.activate
def test_delete_note():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/notes/2",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_note(2)
    assert result["deleted"] is True 