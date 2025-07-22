import responses
from affinity.client import AffinityClient

@responses.activate
def test_whoami():
    responses.add(
        responses.GET,
        "https://api.affinity.co/auth/whoami",
        json={"user": {"id": 1, "email": "user@example.com"}},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.whoami()
    assert "user" in result
    assert result["user"]["email"] == "user@example.com"

@responses.activate
def test_get_rate_limit_status():
    responses.add(
        responses.GET,
        "https://api.affinity.co/rate-limit",
        json={"rate_limit": {"limit": 1000, "remaining": 999}},
        status=200,
    )
    client = AffinityClient(api_key="test")
    result = client.get_rate_limit_status()
    assert "rate_limit" in result
    assert result["rate_limit"]["limit"] == 1000

@responses.activate
def test_get_relationship_strengths():
    responses.add(
        responses.GET,
        "https://api.affinity.co/relationships-strengths",
        json={"strength": 42},
        status=200,
        match_querystring=False
    )
    client = AffinityClient(api_key="test")
    result = client.get_relationship_strengths(external_id=123)
    assert "strength" in result
    assert result["strength"] == 42 