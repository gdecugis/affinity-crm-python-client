import os
from dotenv import load_dotenv
from affinity.client import AffinityClient

load_dotenv()

API_KEY = os.getenv("AFFINITY_API_KEY")

TARGET_DOMAIN = "emmi.ai"

client = AffinityClient(api_key=API_KEY)

print(f"🔍 Searching for organizations with domain: {TARGET_DOMAIN}")
try:
    result = client.list_organizations(term=TARGET_DOMAIN)
    organizations = result.get("organizations", [])
    
    if organizations:
        print(f"✅ Found {len(organizations)} organization(s) with domain '{TARGET_DOMAIN}'")
        
        for org in organizations:
            org_id = org["id"]
            print(f"   📋 Organization: {org['name']} (ID: {org_id})")
            
            # Get the full organization details with opportunities included
            try:
                full_org = client.get_organization(org_id, with_opportunities=True)
                opportunity_ids = full_org.get("opportunity_ids", [])
                
                if opportunity_ids:
                    print(f"   🔍 Found {len(opportunity_ids)} associated opportunity ID(s)")
                    
                    # The opportunities are already included in the response
                    opportunities = full_org.get("opportunities", [])
                    if opportunities:
                        for opportunity in opportunities:
                            print(f"      💼 {opportunity['name']} (ID: {opportunity['id']})")
                    else:
                        # Fallback: fetch opportunities individually if not included
                        for opp_id in opportunity_ids:
                            try:
                                opportunity = client.get_opportunity(opp_id)
                                print(f"      💼 {opportunity['name']} (ID: {opp_id})")
                            except Exception as e:
                                print(f"      ❌ Error retrieving opportunity {opp_id}: {e}")
                    
                    print(f"   📊 Total opportunities: {len(opportunity_ids)}")
                else:
                    print(f"   📝 No opportunities found for this organization")
                    
            except Exception as e:
                print(f"   ❌ Error retrieving organization details: {e}")
                
    else:
        print(f"❌ No organizations found with domain '{TARGET_DOMAIN}'")
        
except Exception as e:
    print(f"❌ Error while searching: {e}")
    exit(1)