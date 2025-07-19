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

    def get_person(self, person_id: int, with_opportunities: bool = False, with_interactions: bool = False, 
                   with_notes: bool = False, with_reminders: bool = False, with_files: bool = False):
        """
        Get a specific person by ID.
        
        Args:
            person_id: The person ID
            with_opportunities: Include opportunities in the response
            with_interactions: Include interactions in the response
            with_notes: Include notes in the response
            with_reminders: Include reminders in the response
            with_files: Include files in the response
        """
        params = {}
        if with_opportunities:
            params["with_opportunities"] = "true"
        if with_interactions:
            params["with_interactions"] = "true"
        if with_notes:
            params["with_notes"] = "true"
        if with_reminders:
            params["with_reminders"] = "true"
        if with_files:
            params["with_files"] = "true"
        return self._request("GET", f"/persons/{person_id}", params=params)

    def list_persons(self, page_size: int = 50, page_token: str = None, term: str = None, 
                     list_id: int = None, organization_id: int = None, opportunity_id: int = None):
        """
        List persons with optional filtering and pagination.
        
        Args:
            page_size: Number of results per page (default: 50)
            page_token: Token for pagination
            term: Search term for filtering persons
            list_id: Filter by list ID
            organization_id: Filter by organization ID
            opportunity_id: Filter by opportunity ID
        """
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        if term:
            params["term"] = term
        if list_id:
            params["list_id"] = list_id
        if organization_id:
            params["organization_id"] = organization_id
        if opportunity_id:
            params["opportunity_id"] = opportunity_id
        return self._request("GET", "/persons", params=params)

    def search_persons(self, term: str, page_size: int = 50, page_token: str = None, 
                       list_id: int = None, organization_id: int = None, opportunity_id: int = None):
        """Search for persons by term (name, email, etc.) with optional filtering."""
        return self.list_persons(page_size=page_size, page_token=page_token, term=term,
                                list_id=list_id, organization_id=organization_id, opportunity_id=opportunity_id)

    def list_all_persons(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_persons(page_size=page_size, page_token=token)
            for person in data.get("persons", []):
                yield person
            token = data.get("next_page_token")
            if not token:
                break

    def create_person(self, data: dict):
        return self._request("POST", "/persons", data=data)

    def update_person(self, person_id: int, data: dict):
        return self._request("PATCH", f"/persons/{person_id}", data=data)

    def delete_person(self, person_id: int):
        return self._request("DELETE", f"/persons/{person_id}")

    # ---------- Organizations ----------

    def get_organization(self, org_id: int, with_opportunities: bool = False, with_persons: bool = False, 
                        with_interactions: bool = False, with_notes: bool = False, 
                        with_reminders: bool = False, with_files: bool = False):
        """
        Get a specific organization by ID.
        
        Args:
            org_id: The organization ID
            with_opportunities: Include opportunities in the response
            with_persons: Include persons in the response
            with_interactions: Include interactions in the response
            with_notes: Include notes in the response
            with_reminders: Include reminders in the response
            with_files: Include files in the response
        """
        params = {}
        if with_opportunities:
            params["with_opportunities"] = "true"
        if with_persons:
            params["with_persons"] = "true"
        if with_interactions:
            params["with_interactions"] = "true"
        if with_notes:
            params["with_notes"] = "true"
        if with_reminders:
            params["with_reminders"] = "true"
        if with_files:
            params["with_files"] = "true"
        return self._request("GET", f"/organizations/{org_id}", params=params)

    def list_organizations(self, page_size: int = 50, page_token: str = None, term: str = None,
                          list_id: int = None, person_id: int = None, opportunity_id: int = None):
        """
        List organizations with optional filtering and pagination.
        
        Args:
            page_size: Number of results per page (default: 50)
            page_token: Token for pagination
            term: Search term for filtering organizations
            list_id: Filter by list ID
            person_id: Filter by person ID
            opportunity_id: Filter by opportunity ID
        """
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        if term:
            params["term"] = term
        if list_id:
            params["list_id"] = list_id
        if person_id:
            params["person_id"] = person_id
        if opportunity_id:
            params["opportunity_id"] = opportunity_id
        return self._request("GET", "/organizations", params=params)

    def search_organizations(self, term: str, page_size: int = 50, page_token: str = None,
                            list_id: int = None, person_id: int = None, opportunity_id: int = None):
        """Search for organizations by term (name, domain, etc.) with optional filtering."""
        return self.list_organizations(page_size=page_size, page_token=page_token, term=term,
                                      list_id=list_id, person_id=person_id, opportunity_id=opportunity_id)

    def list_all_organizations(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_organizations(page_size=page_size, page_token=token)
            for org in data.get("organizations", []):
                yield org
            token = data.get("next_page_token")
            if not token:
                break

    def create_organization(self, data: dict):
        return self._request("POST", "/organizations", data=data)

    def update_organization(self, org_id: int, data: dict):
        return self._request("PATCH", f"/organizations/{org_id}", data=data)

    def delete_organization(self, org_id: int):
        return self._request("DELETE", f"/organizations/{org_id}")

    # ---------- Opportunities ----------

    def get_opportunity(self, opp_id: int, with_interactions: bool = False, with_notes: bool = False, 
                       with_reminders: bool = False, with_files: bool = False):
        """
        Get a specific opportunity by ID.
        
        Args:
            opp_id: The opportunity ID
            with_interactions: Include interactions in the response
            with_notes: Include notes in the response
            with_reminders: Include reminders in the response
            with_files: Include files in the response
        """
        params = {}
        if with_interactions:
            params["with_interactions"] = "true"
        if with_notes:
            params["with_notes"] = "true"
        if with_reminders:
            params["with_reminders"] = "true"
        if with_files:
            params["with_files"] = "true"
        return self._request("GET", f"/opportunities/{opp_id}", params=params)

    def list_opportunities(self, page_size: int = 50, page_token: str = None, term: str = None,
                          list_id: int = None, organization_id: int = None, person_id: int = None):
        """
        List opportunities with optional filtering and pagination.
        
        Args:
            page_size: Number of results per page (default: 50)
            page_token: Token for pagination
            term: Search term for filtering opportunities
            list_id: Filter by list ID
            organization_id: Filter by organization ID
            person_id: Filter by person ID
        """
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        if term:
            params["term"] = term
        if list_id:
            params["list_id"] = list_id
        if organization_id:
            params["organization_id"] = organization_id
        if person_id:
            params["person_id"] = person_id
        return self._request("GET", "/opportunities", params=params)

    def search_opportunities(self, term: str, page_size: int = 50, page_token: str = None,
                            list_id: int = None, organization_id: int = None, person_id: int = None):
        """Search for opportunities by term (name, etc.) with optional filtering."""
        return self.list_opportunities(page_size=page_size, page_token=page_token, term=term,
                                      list_id=list_id, organization_id=organization_id, person_id=person_id)

    def list_all_opportunities(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_opportunities(page_size=page_size, page_token=token)
            for opp in data.get("opportunities", []):
                yield opp
            token = data.get("next_page_token")
            if not token:
                break

    def create_opportunity(self, data: dict):
        return self._request("POST", "/opportunities", data=data)

    def update_opportunity(self, opp_id: int, data: dict):
        return self._request("PATCH", f"/opportunities/{opp_id}", data=data)

    def delete_opportunity(self, opp_id: int):
        return self._request("DELETE", f"/opportunities/{opp_id}")

    # ---------- Lists ----------

    def get_list(self, list_id: int):
        return self._request("GET", f"/lists/{list_id}")

    def list_lists(self):
        return self._request("GET", "/lists")

    # ---------- List Entries ----------

    def get_list_entry(self, entry_id: int):
        return self._request("GET", f"/list-entries/{entry_id}")

    def list_list_entries(self, list_id: int, page_size: int = 50, page_token: str = None,
                         person_id: int = None, organization_id: int = None, opportunity_id: int = None):
        """
        List entries in a specific list with optional filtering and pagination.
        
        Args:
            list_id: The list ID
            page_size: Number of results per page (default: 50)
            page_token: Token for pagination
            person_id: Filter by person ID
            organization_id: Filter by organization ID
            opportunity_id: Filter by opportunity ID
        """
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        if person_id:
            params["person_id"] = person_id
        if organization_id:
            params["organization_id"] = organization_id
        if opportunity_id:
            params["opportunity_id"] = opportunity_id
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

    def add_list_entry(self, list_id: int, data: dict):
        return self._request("POST", f"/lists/{list_id}/list-entries", data=data)

    def delete_list_entry(self, entry_id: int):
        return self._request("DELETE", f"/list-entries/{entry_id}")

    def update_field_values(self, list_id: int, entry_id: int, values: list):
        return self._request("PATCH", f"/lists/{list_id}/list-entries/{entry_id}/field-values", data={"values": values})

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