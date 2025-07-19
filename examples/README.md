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

- The script requires an Affinity API key with appropriate permissions
- Domain search is case-sensitive and exact match
- The script will show all opportunities associated with organizations matching the domain
- Make sure your `.env` file is in the project root directory 