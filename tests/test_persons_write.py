import responses
import pytest
from affinity.client import AffinityClient

@responses.activate
def test_create_person():
    responses.add(
        responses.POST,
        "https://api.affinity.co/persons",
        json={"id": 321, "name": "New Person"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_person(
        first_name="New",
        last_name="Person",
        emails=["new.person@example.com"],
        organization_ids=[123, 456]
    )
    assert result["id"] == 321
    assert result["name"] == "New Person"

@responses.activate
def test_create_person_validation_error():
    client = AffinityClient(api_key="test")
    # Missing required parameter 'emails'
    with pytest.raises(ValueError) as excinfo:
        client.create_person(
            first_name="New",
            last_name="Person",
            emails=None
        )
    assert "Parameter validation error" in str(excinfo.value)
    # Wrong type for emails
    with pytest.raises(ValueError) as excinfo:
        client.create_person(
            first_name="New",
            last_name="Person",
            emails="not-an-email-list"
        )
    assert "Parameter validation error" in str(excinfo.value)

@responses.activate
def test_update_person():
    responses.add(
        responses.PUT,
        "https://api.affinity.co/persons/321",
        json={"id": 321, "name": "Updated Person"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_person(321, first_name="Updated", last_name="Person", emails=["updated.person@example.com"], organization_ids=[789])
    assert result["id"] == 321
    assert result["name"] == "Updated Person"

@responses.activate
def test_delete_person():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/persons/321",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_person(321)
    assert result["deleted"] is True