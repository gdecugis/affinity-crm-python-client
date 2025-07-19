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
- Search for organizations by domain name using Affinity's search API
- Find opportunities associated with those organizations

#### Usage

```bash
python examples/opportunities_for_domain.py
```

#### How it works

1. **Domain Search**: Uses `client.search_organizations(domain)` to efficiently search for organizations by domain
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
- The `list_fields.py` script provides comprehensive field analysis useful for understanding list structure and available options
- Make sure your `.env` file is in the project root directory 