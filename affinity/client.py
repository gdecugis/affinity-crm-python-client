# affinity/client.py

import requests
from requests.auth import HTTPBasicAuth
from pydantic import ValidationError
from typing import List
from affinity.models import CreatePersonParams, UpdatePersonParams, GetPersonParams, ListPersonsParams, CreateOrganizationParams, UpdateOrganizationParams, GetOrganizationParams, ListOrganizationsParams, CreateOpportunityParams, UpdateOpportunityParams, GetOpportunityParams, ListOpportunitiesParams, CreateListParams, GetListEntriesParams, AddListEntryParams, ListFieldsParams, CreateFieldParams, ListFieldValuesParams, ListFieldValueChangesParams, CreateFieldValueParams, UpdateFieldValueParams, CreateNoteParams, UpdateNoteParams, ListNotesParams, CreateInteractionParams, UpdateInteractionParams, ListInteractionsParams, GetInteractionParams, CreateWebhookParams, UpdateWebhookParams, GetWebhookParams, GetRelationshipStrengthsParams

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

    def get_person(self, person_id: int, with_interaction_dates: bool = None, with_interaction_persons: bool = None, with_opportunities: bool = None, with_current_organizations: bool = None):
        """
        Get a specific person by ID, with all documented query parameters.
        """
        try:
            params = GetPersonParams(
                with_interaction_dates=with_interaction_dates,
                with_interaction_persons=with_interaction_persons,
                with_opportunities=with_opportunities,
                with_current_organizations=with_current_organizations
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/persons/{person_id}", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})

    def list_persons(self, term: str = None, with_interaction_dates: bool = None, with_interaction_persons: bool = None, with_opportunities: bool = None, with_current_organizations: bool = None, min_interaction_date: str = None, max_interaction_date: str = None, page_size: int = 50, page_token: str = None):
        """
        List persons with all documented query parameters.
        """
        try:
            params = ListPersonsParams(
                term=term,
                with_interaction_dates=with_interaction_dates,
                with_interaction_persons=with_interaction_persons,
                with_opportunities=with_opportunities,
                with_current_organizations=with_current_organizations,
                min_interaction_date=min_interaction_date,
                max_interaction_date=max_interaction_date,
                page_size=page_size,
                page_token=page_token
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/persons", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})

    def list_all_persons(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_persons(page_size=page_size, page_token=token)
            for person in data.get("persons", []):
                yield person
            token = data.get("next_page_token")
            if not token:
                break

    def create_person(self, first_name, last_name, emails, organization_ids=None):
        try:
            params = CreatePersonParams(
                first_name=first_name,
                last_name=last_name,
                emails=emails,
                organization_ids=organization_ids
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/persons", data=params.model_dump(exclude_none=True))

    def update_person(self, person_id: int, first_name: str = None, last_name: str = None, emails=None, organization_ids=None):
        try:
            params = UpdatePersonParams(
                first_name=first_name,
                last_name=last_name,
                emails=emails,
                organization_ids=organization_ids
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/persons/{person_id}", data=params.model_dump(exclude_none=True))

    def delete_person(self, person_id: int):
        return self._request("DELETE", f"/persons/{person_id}")

    # ---------- Organizations ----------

    def get_organization(self, org_id: int, with_opportunities: bool = None, with_persons: bool = None, with_interactions: bool = None, with_notes: bool = None, with_reminders: bool = None, with_files: bool = None):
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
        try:
            params = GetOrganizationParams(
                with_opportunities=with_opportunities,
                with_persons=with_persons,
                with_interactions=with_interactions,
                with_notes=with_notes,
                with_reminders=with_reminders,
                with_files=with_files
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/organizations/{org_id}", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})

    def list_organizations(self, term: str = None, page_size: int = 50, page_token: str = None, list_id: int = None, person_id: int = None, opportunity_id: int = None):
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
        try:
            params = ListOrganizationsParams(
                term=term,
                page_size=page_size,
                page_token=page_token,
                list_id=list_id,
                person_id=person_id,
                opportunity_id=opportunity_id
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/organizations", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})



    def list_all_organizations(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_organizations(page_size=page_size, page_token=token)
            for org in data.get("organizations", []):
                yield org
            token = data.get("next_page_token")
            if not token:
                break

    def create_organization(self, name: str, domain: str = None):
        try:
            params = CreateOrganizationParams(
                name=name,
                domain=domain
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/organizations", data=params.model_dump(exclude_none=True))

    def update_organization(self, org_id: int, name: str = None, domain: str = None):
        try:
            params = UpdateOrganizationParams(
                name=name,
                domain=domain
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/organizations/{org_id}", data=params.model_dump(exclude_none=True))

    def delete_organization(self, org_id: int):
        return self._request("DELETE", f"/organizations/{org_id}")

    # ---------- Opportunities ----------

    def get_opportunity(self, opp_id: int, with_interactions: bool = None, with_notes: bool = None, with_reminders: bool = None, with_files: bool = None):
        try:
            params = GetOpportunityParams(
                with_interactions=with_interactions,
                with_notes=with_notes,
                with_reminders=with_reminders,
                with_files=with_files
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/opportunities/{opp_id}", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})

    def list_opportunities(self, page_size: int = 50, page_token: str = None, term: str = None, list_id: int = None, organization_id: int = None, person_id: int = None):
        try:
            params = ListOpportunitiesParams(
                page_size=page_size,
                page_token=page_token,
                term=term,
                list_id=list_id,
                organization_id=organization_id,
                person_id=person_id
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/opportunities", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})



    def list_all_opportunities(self, page_size: int = 50):
        token = None
        while True:
            data = self.list_opportunities(page_size=page_size, page_token=token)
            for opp in data.get("opportunities", []):
                yield opp
            token = data.get("next_page_token")
            if not token:
                break

    def create_opportunity(self, name: str, list_id: int, organization_ids: List[int] = None):
        try:
            params = CreateOpportunityParams(
                name=name,
                list_id=list_id,
                organization_ids=organization_ids
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/opportunities", data=params.model_dump(exclude_none=True))

    def update_opportunity(self, opp_id: int, name: str = None):
        try:
            params = UpdateOpportunityParams(
                name=name
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/opportunities/{opp_id}", data=params.model_dump(exclude_none=True))

    def delete_opportunity(self, opp_id: int):
        return self._request("DELETE", f"/opportunities/{opp_id}")

    # ---------- Lists ----------

    def list_lists(self):
        return self._request("GET", "/lists")

    def create_list(self, name: str, type: int, is_public: bool, owner_id: int = None, additional_permissions: list = None):
        try:
            params = CreateListParams(
                name=name,
                type=type,
                is_public=is_public,
                owner_id=owner_id,
                additional_permissions=additional_permissions
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/lists", data=params.model_dump(exclude_none=True))

    def get_list(self, list_id: int):
        return self._request("GET", f"/lists/{list_id}")

    def list_list_entries(self, list_id: int, page_size: int = None, page_token: str = None):
        try:
            params = GetListEntriesParams(
                page_size=page_size,
                page_token=page_token
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/lists/{list_id}/list-entries", params=params.model_dump(exclude_none=True))

    def add_list_entry(self, list_id: int, entity_id: int, creator_id: int = None):
        try:
            params = AddListEntryParams(
                entity_id=entity_id,
                creator_id=creator_id
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", f"/lists/{list_id}/list-entries", data=params.model_dump(exclude_none=True))

    def delete_list_entry(self, list_id: int, list_entry_id: int):
        return self._request("DELETE", f"/lists/{list_id}/list-entries/{list_entry_id}")

    # ---------- List Entries ----------

    def get_list_entry(self, entry_id: int):
        return self._request("GET", f"/list-entries/{entry_id}")

    def list_all_list_entries(self, list_id: int, page_size: int = 50):
        token = None
        while True:
            data = self.list_list_entries(list_id=list_id, page_size=page_size, page_token=token)
            for entry in data.get("list_entries", []):
                yield entry
            token = data.get("next_page_token")
            if not token:
                break

    def create_field_value(self, field_id: int, value, entity_id: int, list_entry_id: int = None):
        try:
            params = CreateFieldValueParams(
                field_id=field_id,
                value=value,
                entity_id=entity_id,
                list_entry_id=list_entry_id
            )
            print(params)
            print(params.model_dump(exclude_none=True))
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/field-values", data=params.model_dump(exclude_none=True))

    def update_field_value(self, field_value_id: int, value):
        try:
            params = UpdateFieldValueParams(
                value=value
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/field-values/{field_value_id}", data=params.model_dump(exclude_none=True))

    def delete_field_value(self, field_value_id: int):
        return self._request("DELETE", f"/field-values/{field_value_id}")

    # ---------- Fields ----------

    def list_fields(self, list_id: int = None, value_type: int = None, entity_type: int = None, with_modified_names: bool = None, exclude_dropdown_options: bool = None, page_size: int = None, page_token: str = None):
        try:
            params = ListFieldsParams(
                list_id=list_id,
                value_type=value_type,
                entity_type=entity_type,
                with_modified_names=with_modified_names,
                exclude_dropdown_options=exclude_dropdown_options,
                page_size=page_size,
                page_token=page_token
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/fields", params={k: str(v).lower() if isinstance(v, bool) else v for k, v in params.model_dump(exclude_none=True).items()})

    def create_field(self, name: str, entity_type: int, value_type: int, list_id: int = None, allows_multiple: bool = None, is_list_specific: bool = None, is_required: bool = None):
        try:
            params = CreateFieldParams(
                name=name,
                entity_type=entity_type,
                value_type=value_type,
                list_id=list_id,
                allows_multiple=allows_multiple,
                is_list_specific=is_list_specific,
                is_required=is_required
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/fields", data=params.model_dump(exclude_none=True))

    def delete_field(self, field_id: int):
        return self._request("DELETE", f"/fields/{field_id}")

    def get_field(self, field_id: int):
        return self._request("GET", f"/fields/{field_id}")

    def list_field_values(self, field_values_query_id: int, field_id: int = None, page_size: int = None, page_token: str = None):
        """
        List field values for a specific entity.
        
        Args:
            field_values_query_id: The ID of the entity (person_id, organization_id, opportunity_id, or list_entry_id)
            field_id: Optional field ID to filter by
            page_size: Number of results per page
            page_token: Token for pagination
        """
        try:
            params = ListFieldValuesParams(
                field_values_query_id=field_values_query_id,
                field_id=field_id,
                page_size=page_size,
                page_token=page_token
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        
        # Convert the abstract parameter to the appropriate API parameter
        api_params = params.model_dump(exclude_none=True)
        query_id = api_params.pop('field_values_query_id')
        
        # The API expects one of these parameters, so we'll try them in order
        # This is a bit of a hack, but it's the simplest way to handle the API requirement
        for param_name in ['person_id', 'organization_id', 'opportunity_id', 'list_entry_id']:
            api_params[param_name] = query_id
            break  # Just use the first one - the API will validate if it's correct
        
        return self._request("GET", "/field-values", params=api_params)

    def list_field_value_changes(self, field_id: int, field_value_changes_query_id: int, action_type: int = None):
        """
        List field value changes for a specific entity.
        
        Args:
            field_id: The ID of the field to get changes for
            field_value_changes_query_id: The ID of the entity (person_id, organization_id, opportunity_id, or list_entry_id)
            action_type: Optional action type filter (e.g., 1 = added, 2 = removed)
        """
        try:
            params = ListFieldValueChangesParams(
                field_id=field_id,
                field_value_changes_query_id=field_value_changes_query_id,
                action_type=action_type
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        
        # Convert the abstract parameter to the appropriate API parameter
        api_params = params.model_dump(exclude_none=True)
        query_id = api_params.pop('field_value_changes_query_id')
        
        # The API expects one of these parameters, so we'll try them in order
        for param_name in ['person_id', 'organization_id', 'opportunity_id', 'list_entry_id']:
            api_params[param_name] = query_id
            break  # Just use the first one - the API will validate if it's correct
        
        return self._request("GET", "/field-value-changes", params=api_params)

    # ---------- Notes ----------

    def list_notes(self, entity_id: int, entity_type: str):
        try:
            params = ListNotesParams(
                entity_id=entity_id,
                entity_type=entity_type
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/notes", params=params.model_dump(exclude_none=True))

    def create_note(self, note: str, creator_id: int, entity_id: int, entity_type: str):
        try:
            params = CreateNoteParams(
                note=note,
                creator_id=creator_id,
                entity_id=entity_id,
                entity_type=entity_type
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/notes", data=params.model_dump(exclude_none=True))

    def update_note(self, note_id: int, note: str = None):
        try:
            params = UpdateNoteParams(
                note=note
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/notes/{note_id}", data=params.model_dump(exclude_none=True))

    def delete_note(self, note_id: int):
        return self._request("DELETE", f"/notes/{note_id}")

    # ---------- Interactions ----------

    def list_interactions(self, person_id: int = None, organization_id: int = None, opportunity_id: int = None, list_entry_id: int = None):
        try:
            params = ListInteractionsParams(
                person_id=person_id,
                organization_id=organization_id,
                opportunity_id=opportunity_id,
                list_entry_id=list_entry_id
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", "/interactions", params=params.model_dump(exclude_none=True))

    def get_interaction(self, interaction_id: int, type: str):
        """
        Get a specific interaction by ID with type parameter.
        
        Args:
            interaction_id: The interaction ID
            type: Type of the list (e.g., People = 0, Organizations = 1, Opportunities = 2)
        """
        try:
            params = GetInteractionParams(type=type)
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/interactions/{interaction_id}", params=params.model_dump(exclude_none=True))

    def create_interaction(self, interaction_type: str, subject: str, date: str, creator_id: int, participants: list, entity_id: int, entity_type: str, notes: str = None):
        try:
            params = CreateInteractionParams(
                interaction_type=interaction_type,
                subject=subject,
                date=date,
                creator_id=creator_id,
                participants=participants,
                entity_id=entity_id,
                entity_type=entity_type,
                notes=notes
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/interactions", data=params.model_dump(exclude_none=True))

    def update_interaction(self, interaction_id: int, interaction_type: str = None, subject: str = None, date: str = None, creator_id: int = None, participants: list = None, entity_id: int = None, entity_type: str = None, notes: str = None):
        try:
            params = UpdateInteractionParams(
                interaction_type=interaction_type,
                subject=subject,
                date=date,
                creator_id=creator_id,
                participants=participants,
                entity_id=entity_id,
                entity_type=entity_type,
                notes=notes
            )
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/interactions/{interaction_id}", data=params.model_dump(exclude_none=True))

    def delete_interaction(self, interaction_id: int):
        return self._request("DELETE", f"/interactions/{interaction_id}")

    # ---------- Webhooks ----------

    def create_webhook(self, url: str, event: str):
        try:
            params = CreateWebhookParams(url=url, event=event)
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("POST", "/webhook/subscribe", data=params.model_dump(exclude_none=True))

    def get_webhook(self, webhook_subscription_id: str = None):
        if webhook_subscription_id:
            return self._request("GET", f"/webhook/{webhook_subscription_id}")
        else:
            return self._request("GET", "/webhook")

    def update_webhook(self, webhook_subscription_id: str, url: str = None, event: str = None):
        try:
            params = UpdateWebhookParams(url=url, event=event)
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("PUT", f"/webhook/{webhook_subscription_id}", data=params.model_dump(exclude_none=True))

    def delete_webhook(self, webhook_subscription_id: str):
        return self._request("DELETE", f"/webhook/{webhook_subscription_id}")

    # ---------- Utility ----------

    def whoami(self):
        return self._request("GET", "/auth/whoami")

    def get_rate_limit_status(self):
        return self._request("GET", "/rate-limit")

    def get_relationship_strengths(self, external_id: int):
        try:
            params = GetRelationshipStrengthsParams(external_id=external_id)
        except ValidationError as e:
            raise ValueError(f"Parameter validation error: {e}")
        return self._request("GET", f"/relationships-strengths", params=params.model_dump(exclude_none=True))

    # ---------- Wrappers & Added functions ----------

    def set_field_value(self, field_id, value, entity_id, list_entry_id=None):
        """
        Smart method that either creates or updates a field value.
        First checks if a field value exists, then creates or updates accordingly.
        Args:
            field_id: The field ID
            value: The field value
            entity_id: The entity ID
            list_entry_id: The list entry ID (optional but often required)
        """
        # First, try to get existing field values for this entity and field
        try:
            field_values = self.list_field_values(entity_id, field_id=field_id)
            existing_values = field_values.get("field_values", [])
            
            if existing_values:
                # Update existing field value
                field_value_id = existing_values[0]["id"]
                return self.update_field_value(field_value_id, value)
            else:
                # Create new field value
                return self.create_field_value(field_id, value, entity_id, list_entry_id)
                
        except Exception as e:
            # If we can't determine existing values, just try to create
            return self.create_field_value(field_id, value, entity_id, list_entry_id)