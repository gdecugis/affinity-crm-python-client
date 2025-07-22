# Affinity CRM Python Client - Examples

This directory contains example scripts demonstrating how to use the Affinity CRM Python client.

## Prerequisites

1. Install the affinity-crm-python-client package and dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

2. Get your Affinity API key from your Affinity workspace settings.

3. Set up your environment variables:
   
   Create a `.env` file in the project root with your API key:
   ```bash
   # .env
   AFFINITY_API_KEY=your_actual_affinity_api_key_here
   ```

## Available Examples

### opportunities_for_domain.py

This script demonstrates how to:
- Search for organizations by domain name using Affinity's list API
- Find opportunities associated with those organizations

#### Usage

```bash
python examples/opportunities_for_domain.py
```

#### How it works

1. **Domain Search**: Uses `client.list_organizations(term=domain)` to efficiently search for organizations by domain
2. **Opportunity Retrieval**: For matching organizations, searches for opportunities by organization name and filters by `organization_ids`

#### Example Output

```
Found organization: Example Corp (ID: 123)

Associated Opportunities:
- Series A Investment (ID: 456)
- Partnership Discussion (ID: 457)
```

#### Customization

To search for a different domain, modify the `TARGET_DOMAIN` variable in the script:

```python
TARGET_DOMAIN = "your-target-domain.com"
```

### list_fields.py

This script demonstrates how to:
- Retrieve all fields for a specific list
- Display detailed field information including types, requirements, and properties
- Show dropdown options and their metadata for the first field in the list

#### Usage

```bash
python examples/list_fields.py
```

#### How it works

1. **List Details**: Gets list information using `client.get_list(list_id)` to retrieve list name and description
2. **Field Retrieval**: Uses `client.list_fields(list_id=LIST_ID)` to get all fields for the specified list
3. **Field Analysis**: Displays comprehensive field information including:
   - Field name, ID, and type
   - Required/optional status
   - Type-specific properties (dropdown options, number ranges, etc.)
4. **Dropdown Options**: Shows all possible values for the first field with their metadata (ID, text, rank, color)

#### Example Output

```
📋 List: Deal Pipeline (ID: 263367)
   📝 Description: Active deals in our pipeline

📊 Found 15 fields for list 263367:

   1. Status
      🆔 ID: 4707433
      📝 Type: dropdown
      🟢 Optional
      📋 Options: Identified, Qualified, Study, Partners Meeting, Term Sheet, Portfolio Company, To Be Dropped, Dropped, Lost, To Contact Again

🔍 Getting all possible values for the first field: Status (ID: 4707433)

📋 Found 10 possible values for field 'Status':

   1. Identified
      🆔 Option ID: 19697139
      📊 Rank: 1
      🎨 Color: 1

   2. Qualified
      🆔 Option ID: 19697146
      📊 Rank: 2
      🎨 Color: 2
```

#### Customization

To analyze a different list, modify the `LIST_ID` variable in the script:

```python
LIST_ID = 123456  # Replace with your target list ID
```

### create_opportunity_workflow.py

This script demonstrates a complete workflow for:
- Checking if an organization exists for a specific domain
- Creating the organization if it doesn't exist and adding it to a list
- Creating an opportunity associated with the organization
- Setting custom field values for the opportunity with proper field type handling

#### Usage

```bash
python examples/create_opportunity_workflow.py
```

#### How it works

1. **Organization Check**: Uses `client.list_organizations(term=domain)` to check if an organization exists for the target domain
2. **Organization Creation**: If not found, creates a new organization using `client.create_organization()` with domain and name
3. **List Assignment**: Adds the organization to the target list using `client.add_list_entry()`
4. **Opportunity Creation**: Creates a new opportunity using `client.create_opportunity()` with basic information
5. **List Entry**: Adds the opportunity to the target list as a list entry
6. **Field Values**: Sets custom field values using `client.update_field_values()` with proper field type handling:
   - **Dropdown fields** (value_type 2, 7): Use dropdown option IDs
   - **Person fields** (value_type 0): Use person IDs
   - **Number fields** (value_type 3): Use numeric values
   - **Text fields** (value_type 6): Use string values

#### Example Output

```
🚀 Starting Affinity workflow for domain: example.com
============================================================
🔍 Checking if organization exists for domain: example.com
❌ No organization found for domain: example.com
🏗️  Creating new organization for domain: example.com
✅ Created organization: Example Inc (ID: 12345)
📋 Adding organization 12345 to list 263367
✅ Added organization to list (Entry ID: 67890)
💼 Creating opportunity for organization: Example Inc
✅ Created opportunity: Investment Opportunity - Example Inc (ID: 11111)
✅ Added opportunity to list (Entry ID: 22222)
🔧 Setting custom field values...
   📝 status: 19697139
   📝 deal_owner: 194355246
   📝 current_deal_stage: 19060786
   📝 origination_serena: 16898335
   📝 deal_fund: 15117961
   📝 origin: 19268510
   📝 fundraising_amount: 2500000
✅ Updated 7 field values

🎉 Workflow completed successfully!
📊 Summary:
   Organization: Example Inc (ID: 12345)
   Opportunity: Investment Opportunity - Example Inc (ID: 11111)
   List: 263367
   Custom fields set: 7
```

#### Customization

To customize the workflow, modify these variables in the script:

```python
TARGET_DOMAIN = "your-target-domain.com"  # Domain to check/create
LIST_ID = 263367  # Target list ID

# Field configurations - modify field IDs and values as needed
FIELD_CONFIG = {
    "status": {
        "field_id": 4707433,
        "value_type": 7,  # Dropdown
        "value": 19697139  # "Identified" option ID
    },
    # ... other fields
}
```

#### Field Value Types

The script handles different field value types according to the [Affinity API documentation](https://api-docs.affinity.co/#the-field-resource):

- **Type 0 (Person)**: Use person ID (e.g., `194355246`)
- **Type 2 (Dropdown)**: Use dropdown option ID (e.g., `16898335`)
- **Type 3 (Number)**: Use numeric value (e.g., `2500000`)
- **Type 6 (Text)**: Use string value (e.g., `"Some text"`)
- **Type 7 (Dropdown)**: Use dropdown option ID (e.g., `19697139`)

## Environment Setup

The examples use environment variables for secure API key management:

1. **Create `.env` file**: Copy the example below and add your actual API key
   ```
   AFFINITY_API_KEY=your_actual_affinity_api_key_here
   ```

2. **Install dependencies**: Make sure `python-dotenv` is installed
   ```bash
   pip install python-dotenv
   ```

3. **Security**: Never commit your `.env` file to version control. It's already in `.gitignore`.

## Notes

- The scripts require an Affinity API key with appropriate permissions
- Domain search is case-sensitive and exact match
- The `opportunities_for_domain.py` script will show all opportunities associated with organizations matching the domain
- The `create_opportunity_workflow.py` script demonstrates a complete end-to-end workflow for creating opportunities with custom fields
- Field value types must match the field configuration in your Affinity workspace
- List IDs and field IDs are specific to your Affinity workspace and must be obtained from your workspace 