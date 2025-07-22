import os
from dotenv import load_dotenv
from affinity.client import AffinityClient

load_dotenv()

API_KEY = os.getenv("AFFINITY_API_KEY")
TARGET_DOMAIN = "positronic.vc"  # Replace by an actual domain
LIST_ID = 263367  # Use the list ID of the list you want to add the opportunity to

# Sample field configurations for the opportunity with various field types
FIELD_CONFIG = {
    "status": {
        "field_id": 4707433,
        "value_type": 7,  # Dropdown
        "value": 19697139  # "Identified" option ID
    },
    "deal_owner": {
        "field_id": 4707435,
        "value_type": 0,  # Person
        "value": 194355246  # Person ID
    },
    "current_deal_stage": {
        "field_id": 5000141,
        "value_type": 7,  # Dropdown
        "value": 19060786  # "Stealth" 
    },
    "origination_serena": {
        "field_id": 4707483,
        "value_type": 2,  # Dropdown
        "value": "Guillaume Decugis"  # Dropdown option text
    },
    "deal_fund": {
        "field_id": 4707461,
        "value_type": 2,  # Dropdown
        "value": "Data Ventures II"  # Dropdown option text
    },
    "origin": {
        "field_id": 4707487,
        "value_type": 2,  # Dropdown
        "value": "Serena Huntress"  # Dropdown option text
    },
    "fundraising_amount": {
        "field_id": 4707434,
        "value_type": 3,  # Number
        "value": 2500000  # Amount in euros
    }
}

client = AffinityClient(api_key=API_KEY)

def check_organization_exists(domain):
    """Check if an organization exists for the given domain."""
    print(f"🔍 Checking if organization exists for domain: {domain}")
    
    try:
        result = client.list_organizations(term=domain)
        organizations = result.get("organizations", [])
        
        if organizations:
            org = organizations[0]  # Take the first match
            print(f"✅ Found existing organization: {org['name']} (ID: {org['id']})")
            return org
        else:
            print(f"❌ No organization found for domain: {domain}")
            return None
            
    except Exception as e:
        print(f"❌ Error searching for organization: {e}")
        return None



def create_organization(domain):
    """Create a new organization for the given domain."""
    print(f"🏗️  Creating new organization for domain: {domain}")
    
    # Extract company name from domain
    company_name = domain.split('.')[0].title() + " Inc"
    
    org_data = {
        "name": company_name,
        "domain": domain
    }
    
    try:
        new_org = client.create_organization(name=company_name, domain=domain)
        print(f"✅ Created organization: {new_org['name']} (ID: {new_org['id']})")
        return new_org
    except Exception as e:
        print(f"❌ Error creating organization: {e}")
        return None

def add_organization_to_list(org_id, list_id):
    print(f"📋 Adding organization {org_id} to list {list_id}")
    
    try:
        result = client.add_list_entry(list_id, entity_id=org_id)
        print(f"✅ Added organization to list (Entry ID: {result['id']})")
        return result
    except Exception as e:
        print(f"❌ Error adding organization to list: {e}")
        return None

def create_opportunity_with_fields(org_id, org_name, list_id):
    # Create an opportunity with custom field values in 2 steps as the API doesn't support creating with custom fields in one call
    print(f"💼 Creating opportunity for organization: {org_name}")
    
    # Step 1: Create basic opportunity (no custom fields yet)
    try:
        # Step 1: Create the opportunity
        new_opportunity = client.create_opportunity(
            name=f"API Test Opportunity - {org_name}",
            list_id=list_id,
            organization_ids=[org_id]
        )
        opportunity_id = new_opportunity['id']
        print(f"✅ Created opportunity: {new_opportunity['name']} (ID: {opportunity_id})")
        
        # Step 2: Get the list entry ID from the opportunity response
        list_entry_id = new_opportunity['list_entries'][0]['id']
        print(f"✅ List entry ID: {list_entry_id}")
        
        # Step 3: Create field values
        print("🔧 Setting custom field values...")
        field_values_created = 0
        
        for field_name, config in FIELD_CONFIG.items():
            try:
                print(config["field_id"], config["value"], opportunity_id, list_entry_id)
                result = client.set_field_value(
                    field_id=config["field_id"],
                    value=config["value"],
                    entity_id=opportunity_id,
                    list_entry_id=list_entry_id
                )
                print(f"   ✅ {field_name}: {config['value']}")
                field_values_created += 1
            except Exception as e:
                print(f"   ❌ {field_name}: Error - {e}")
        
        print(f"✅ Created {field_values_created} field values")
        
        return new_opportunity
        
    except Exception as e:
        print(f"❌ Error creating opportunity: {e}")
        return None

def main():
    """Main workflow function."""
    print(f"🚀 Starting Affinity workflow for domain: {TARGET_DOMAIN}")
    print("=" * 60)
    
    # Step 1: Check if organization exists
    existing_org = check_organization_exists(TARGET_DOMAIN)
    
    if existing_org:
        org_id = existing_org['id']
        org_name = existing_org['name']
        print(f"📋 Using existing organization: {org_name} (ID: {org_id})")
    else:
        # Step 2: Create organization if it doesn't exist
        new_org = create_organization(TARGET_DOMAIN)
        if not new_org:
            print("❌ Failed to create organization. Exiting.")
            return
        
        org_id = new_org['id']
        org_name = new_org['name']
        
        # Step 3: Add organization to list
        list_entry = add_organization_to_list(org_id, LIST_ID)
        if not list_entry:
            print("⚠️  Warning: Failed to add organization to list, but continuing...")
    
    # Step 4: Create opportunity with custom fields
    opportunity = create_opportunity_with_fields(org_id, org_name, LIST_ID)
    
    if opportunity:
        print("\n🎉 Workflow completed successfully!")
        print(f"📊 Summary:")
        print(f"   Organization: {org_name} (ID: {org_id})")
        print(f"   Opportunity: {opportunity['name']} (ID: {opportunity['id']})")
        print(f"   List: {LIST_ID}")
        print(f"   Custom fields set: {len(FIELD_CONFIG)}")
    else:
        print("\n❌ Workflow failed at opportunity creation step.")

if __name__ == "__main__":
    main() 