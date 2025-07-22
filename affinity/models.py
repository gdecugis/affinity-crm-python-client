from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Union

class CreatePersonParams(BaseModel):
    first_name: str
    last_name: str
    emails: List[EmailStr]
    organization_ids: Optional[List[int]] = None

class UpdatePersonParams(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    emails: Optional[List[EmailStr]] = None
    organization_ids: Optional[List[int]] = None

class GetPersonParams(BaseModel):
    with_interaction_dates: Optional[bool] = None
    with_interaction_persons: Optional[bool] = None
    with_opportunities: Optional[bool] = None
    with_current_organizations: Optional[bool] = None

class ListPersonsParams(BaseModel):
    term: Optional[str] = None
    with_interaction_dates: Optional[bool] = None
    with_interaction_persons: Optional[bool] = None
    with_opportunities: Optional[bool] = None
    with_current_organizations: Optional[bool] = None
    min_interaction_date: Optional[str] = Field(None, alias="min_{interaction_type}_date")
    max_interaction_date: Optional[str] = Field(None, alias="max_{interaction_type}_date")
    page_size: Optional[int] = None
    page_token: Optional[str] = None 

class CreateOrganizationParams(BaseModel):
    name: str
    domain: Optional[str] = None

class UpdateOrganizationParams(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None

class GetOrganizationParams(BaseModel):
    with_opportunities: Optional[bool] = None
    with_persons: Optional[bool] = None
    with_interactions: Optional[bool] = None
    with_notes: Optional[bool] = None
    with_reminders: Optional[bool] = None
    with_files: Optional[bool] = None

class ListOrganizationsParams(BaseModel):
    term: Optional[str] = None
    page_size: Optional[int] = None
    page_token: Optional[str] = None
    list_id: Optional[int] = None
    person_id: Optional[int] = None
    opportunity_id: Optional[int] = None 

class CreateOpportunityParams(BaseModel):
    name: str
    list_id: int
    organization_ids: Optional[List[int]] = None

class UpdateOpportunityParams(BaseModel):
    name: Optional[str] = None

class GetOpportunityParams(BaseModel):
    with_interactions: Optional[bool] = None
    with_notes: Optional[bool] = None
    with_reminders: Optional[bool] = None
    with_files: Optional[bool] = None

class ListOpportunitiesParams(BaseModel):
    page_size: Optional[int] = None
    page_token: Optional[str] = None
    term: Optional[str] = None
    list_id: Optional[int] = None
    organization_id: Optional[int] = None
    person_id: Optional[int] = None 

class CreateListParams(BaseModel):
    name: str
    type: int
    is_public: bool
    owner_id: Optional[int] = None
    additional_permissions: Optional[list] = None

class GetListEntriesParams(BaseModel):
    page_size: Optional[int] = None
    page_token: Optional[str] = None

class AddListEntryParams(BaseModel):
    entity_id: int
    creator_id: Optional[int] = None 

class ListFieldsParams(BaseModel):
    list_id: Optional[int] = None
    value_type: Optional[int] = None
    entity_type: Optional[int] = None
    with_modified_names: Optional[bool] = None
    exclude_dropdown_options: Optional[bool] = None
    page_size: Optional[int] = None
    page_token: Optional[str] = None

class CreateFieldParams(BaseModel):
    name: str
    entity_type: int
    value_type: int
    list_id: Optional[int] = None
    allows_multiple: Optional[bool] = None
    is_list_specific: Optional[bool] = None
    is_required: Optional[bool] = None

class ListFieldValuesParams(BaseModel):
    field_values_query_id: int
    field_id: Optional[int] = None
    page_size: Optional[int] = None
    page_token: Optional[str] = None

class ListFieldValueChangesParams(BaseModel):
    field_id: int
    field_value_changes_query_id: int
    action_type: Optional[int] = None

class CreateFieldValueParams(BaseModel):
    field_id: int
    value: Union[str, int, float, bool, list, dict]
    entity_id: int
    list_entry_id: Optional[int] = None

class UpdateFieldValueParams(BaseModel):
    value: Union[str, int, float, bool, list, dict] 

class CreateNoteParams(BaseModel):
    note: str
    creator_id: int
    entity_id: int
    entity_type: str

class UpdateNoteParams(BaseModel):
    note: Optional[str] = None

class ListNotesParams(BaseModel):
    entity_id: int
    entity_type: str

class CreateInteractionParams(BaseModel):
    interaction_type: str
    subject: str
    date: str
    creator_id: int
    participants: list
    entity_id: int
    entity_type: str
    notes: Optional[str] = None

class UpdateInteractionParams(BaseModel):
    interaction_type: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    creator_id: Optional[int] = None
    participants: Optional[list] = None
    entity_id: Optional[int] = None
    entity_type: Optional[str] = None
    notes: Optional[str] = None

class ListInteractionsParams(BaseModel):
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    opportunity_id: Optional[int] = None
    list_entry_id: Optional[int] = None 

class CreateWebhookParams(BaseModel):
    url: str
    event: str

class UpdateWebhookParams(BaseModel):
    url: Optional[str] = None
    event: Optional[str] = None

class GetWebhookParams(BaseModel):
    webhook_subscription_id: str

class GetRelationshipStrengthsParams(BaseModel):
    external_id: int

class GetInteractionParams(BaseModel):
    type: str

# Rate Limits and Whoami endpoints do not require parameters. 