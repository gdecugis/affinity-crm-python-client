# affinity/client.py

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://api.affinity.co"

class AffinityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, path: str, params=None, data=None):
        url = f"{BASE_URL}{path}"
        auth = HTTPBasicAuth('', self.api_key)
        response = self.session.request(method, url, auth=auth, params=params, json=data)

        if not response.ok:
            raise Exception(f"Affinity API error {response.status_code}: {response.text}")

        return response.json()

    # ---------- Persons ----------

    def get_person(self, person_id: int):
        return self._request("GET", f"/persons/{person_id}")

    def list_persons(self, page_size: int = 50, page_token: str = None):
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", "/persons", params=params)

    def list_all_persons(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_persons(page_size=page_size, page_token=token)
            for person in data.get("persons", []):
                yield person
            token = data.get("next_page_token")
            if not token:
                break

    # ---------- Organizations ----------

    def get_organization(self, org_id: int):
        return self._request("GET", f"/organizations/{org_id}")

    def list_organizations(self, page_size: int = 50, page_token: str = None):
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", "/organizations", params=params)

    def list_all_organizations(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_organizations(page_size=page_size, page_token=token)
            for org in data.get("organizations", []):
                yield org
            token = data.get("next_page_token")
            if not token:
                break

    # ---------- Opportunities ----------

    def get_opportunity(self, opp_id: int):
        return self._request("GET", f"/opportunities/{opp_id}")

    def list_opportunities(self, page_size: int = 50, page_token: str = None):
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", "/opportunities", params=params)

    def list_all_opportunities(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_opportunities(page_size=page_size, page_token=token)
            for opp in data.get("opportunities", []):
                yield opp
            token = data.get("next_page_token")
            if not token:
                break

    # ---------- Lists ----------

    def get_list(self, list_id: int):
        return self._request("GET", f"/lists/{list_id}")

    def list_lists(self):
        return self._request("GET", "/lists")

    # ---------- List Entries ----------

    def get_list_entry(self, entry_id: int):
        return self._request("GET", f"/list-entries/{entry_id}")

    def list_list_entries(self, list_id: int, page_size: int = 50, page_token: str = None):
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        return self._request("GET", f"/lists/{list_id}/list-entries", params=params)

    def list_all_list_entries(self, list_id: int, page_size: int = 50):
        token = None
        while True:
            data = self.list_list_entries(list_id=list_id, page_size=page_size, page_token=token)
            for entry in data.get("list_entries", []):
                yield entry
            token = data.get("next_page_token")
            if not token:
                break

    # ---------- Fields ----------

    def list_fields(self):
        return self._request("GET", "/fields")

    def get_field(self, field_id: int):
        return self._request("GET", f"/fields/{field_id}")

    # ---------- Utility ----------

    def whoami(self):
        return self._request("GET", "/auth/whoami")

    def get_relationship_strengths(self, external_id: int):
        return self._request("GET", f"/relationships-strengths?external_id={external_id}")

    def get_rate_limit_status(self):
        return self._request("GET", "/rate-limit")