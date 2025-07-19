import os
from dotenv import load_dotenv
from affinity.client import AffinityClient

load_dotenv()

API_KEY = os.getenv("AFFINITY_API_KEY")

TARGET_DOMAIN = "emmi.ai"

client = AffinityClient(api_key=API_KEY)

print(f"🔍 Searching for organizations with domain: {TARGET_DOMAIN}")
try:
    result = client.search_organizations(TARGET_DOMAIN)
    organizations = result.get("organizations", [])
    
    if organizations:
        print(f"✅ Found {len(organizations)} organization(s) with domain '{TARGET_DOMAIN}'")
        
        for org in organizations:
            org_id = org["id"]
            print(f"   📋 Organization: {org['name']} (ID: {org_id})")
            
            opp_count = 0
            
            opp_result = client.search_opportunities(org['name'])
            opportunities = opp_result.get("opportunities", [])
            
            for opp in opportunities:
                if org_id in opp.get("organization_ids", []):
                    opp_count += 1
                    print(f"      💼 {opp['name']} (ID: {opp['id']})")
            
            if opp_count == 0:
                print(f"      📝 No opportunities found for this organization")
            else:
                print(f"      📊 Total opportunities: {opp_count}")
                
    else:
        print(f"❌ No organizations found with domain '{TARGET_DOMAIN}'")
        
except Exception as e:
    print(f"❌ Error while searching: {e}")
    exit(1)