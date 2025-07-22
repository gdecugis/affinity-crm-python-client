import responses
from affinity.client import AffinityClient

@responses.activate
def test_create_webhook():
    responses.add(
        responses.POST,
        "https://api.affinity.co/webhook/subscribe",
        json={"id": "abc123", "url": "https://example.com/webhook", "event": "note.created"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.create_webhook(url="https://example.com/webhook", event="note.created")
    assert result["id"] == "abc123"
    assert result["url"] == "https://example.com/webhook"
    assert result["event"] == "note.created"

@responses.activate
def test_get_webhook():
    responses.add(
        responses.GET,
        "https://api.affinity.co/webhook/abc123",
        json={"id": "abc123", "url": "https://example.com/webhook", "event": "note.created"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_webhook(webhook_subscription_id="abc123")
    assert result["id"] == "abc123"
    assert result["url"] == "https://example.com/webhook"
    assert result["event"] == "note.created"

@responses.activate
def test_update_webhook():
    responses.add(
        responses.PUT,
        "https://api.affinity.co/webhook/abc123",
        json={"id": "abc123", "url": "https://example.com/webhook", "event": "note.updated"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.update_webhook("abc123", url="https://example.com/webhook", event="note.updated")
    assert result["id"] == "abc123"
    assert result["event"] == "note.updated"

@responses.activate
def test_delete_webhook():
    responses.add(
        responses.DELETE,
        "https://api.affinity.co/webhook/abc123",
        json={"deleted": True},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.delete_webhook("abc123")
    assert result["deleted"] is True 