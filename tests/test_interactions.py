import responses
from affinity.client import AffinityClient

@responses.activate
def test_list_interactions():
    responses.add(
        responses.GET,
        "https://api.affinity.co/interactions",
        json={"interactions": [{"id": 1, "interaction_type": "email"}]},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.list_interactions(person_id=123)
    assert "interactions" in result
    assert len(result["interactions"]) == 1
    assert result["interactions"][0]["interaction_type"] == "email"

@responses.activate
def test_create_interaction():
    responses.add(
        responses.POST,
        "https://api.affinity.co/interactions",
        json={"id": 2, "interaction_type": "meeting"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_interaction(
        interaction_type="meeting",
        subject="Project Kickoff",
        date="2024-07-01T10:00:00Z",
        creator_id=1,
        participants=[1, 2],
        entity_id=123,
        entity_type="organization",
        notes="Initial meeting"
    )
    assert result["id"] == 2
    assert result["interaction_type"] == "meeting"

@responses.activate
def test_update_interaction():
    responses.add(
        responses.PUT,
        "https://api.affinity.co/interactions/2",
        json={"id": 2, "interaction_type": "call"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_interaction(2, interaction_type="call")
    assert result["id"] == 2
    assert result["interaction_type"] == "call"

@responses.activate
def test_delete_interaction():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/interactions/2",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_interaction(2)
    assert result["deleted"] is True

@responses.activate
def test_get_interaction():
    responses.add(
        responses.GET,
        "https://api.affinity.co/interactions/123?type=0",
        json={"id": 123, "interaction_type": "email", "subject": "Test Email"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_interaction(123, "0")
    assert result["id"] == 123
    assert result["interaction_type"] == "email"
    assert result["subject"] == "Test Email" 