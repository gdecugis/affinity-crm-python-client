import responses
from affinity.client import AffinityClient

@responses.activate
def test_whoami():
    responses.add(
        responses.GET,
        "https://api.affinity.co/auth/whoami",
        json={"id": 1, "email": "guillaume@serena.vc"},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.whoami()
    assert result["email"] == "guillaume@serena.vc"

@responses.activate
def test_get_relationship_strengths():
    responses.add(
        responses.GET,
        "https://api.affinity.co/relationships-strengths?external_id=123",
        json={"external_id": 123, "scores": [{"organization_id": 99, "score": 0.7}]},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_relationship_strengths(123)
    assert result["external_id"] == 123
    assert isinstance(result["scores"], list)

@responses.activate
def test_get_rate_limit_status():
    responses.add(
        responses.GET,
        "https://api.affinity.co/rate-limit",
        json={"daily_limit": 150000, "remaining": 149997},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_rate_limit_status()
    assert result["daily_limit"] == 150000
    assert result["remaining"] == 149997