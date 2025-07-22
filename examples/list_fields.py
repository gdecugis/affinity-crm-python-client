import os
from dotenv import load_dotenv
from affinity.client import AffinityClient

load_dotenv()

API_KEY = os.getenv("AFFINITY_API_KEY")
LIST_ID = 263367

client = AffinityClient(api_key=API_KEY)

print(f"🔍 Listing fields for list ID: {LIST_ID}")

try:
    # Get the list details which includes the fields
    list_details = client.get_list(LIST_ID)
    
    print(f"📋 List: {list_details.get('name', 'Unknown')} (ID: {LIST_ID})")
    print(f"   📝 Description: {list_details.get('description', 'No description')}")
    print()
    
    # Get fields from the list response
    fields = list_details.get("fields", [])
    
    if fields:
        print(f"📊 Found {len(fields)} fields for list {LIST_ID}:")
        print()
        
        # Track dropdown fields for detailed analysis
        dropdown_fields = []
        
        for i, field in enumerate(fields, 1):
            field_id = field.get("id")
            field_name = field.get("name", "Unnamed Field")
            field_type = field.get("type", "Unknown")
            field_required = field.get("required", False)
            
            print(f"   {i}. {field_name}")
            print(f"      🆔 ID: {field_id}")
            print(f"      📝 Type: {field_type}")
            print(f"      {'🔴 Required' if field_required else '🟢 Optional'}")
            
            # Show additional field properties based on type
            if field_type == "dropdown":
                options = field.get("dropdown_options", [])
                if options:
                    print(f"      📋 Options: {len(options)} dropdown options available")
                    dropdown_fields.append(field)
                else:
                    print(f"      📋 Options: None")
            elif field_type == "number":
                min_val = field.get("min_value")
                max_val = field.get("max_value")
                if min_val is not None or max_val is not None:
                    print(f"      📊 Range: {min_val or 'no min'} to {max_val or 'no max'}")
            
            print()
        
        # Now show detailed dropdown options for all dropdown fields
        if dropdown_fields:
            print(f"🔍 Detailed dropdown options for {len(dropdown_fields)} dropdown fields:")
            print("=" * 80)
            
            for field in dropdown_fields:
                field_id = field.get("id")
                field_name = field.get("name", "Unnamed Field")
                dropdown_options = field.get("dropdown_options", [])
                
                print(f"📋 Field: {field_name} (ID: {field_id})")
                print(f"   📊 {len(dropdown_options)} options available:")
                print()
                
                for i, option in enumerate(dropdown_options, 1):
                    option_id = option.get("id")
                    option_text = option.get("text", "No text")
                    option_rank = option.get("rank", "No rank")
                    option_color = option.get("color", "No color")
                    
                    print(f"   {i}. {option_text}")
                    print(f"      🆔 Option ID: {option_id}")
                    print(f"      📊 Rank: {option_rank}")
                    print(f"      🎨 Color: {option_color}")
                    print()
                
                print("-" * 80)
        else:
            print("📝 No dropdown fields found in this list")
            
    else:
        print(f"📝 No fields found for list {LIST_ID}")
        print("   This could mean:")
        print("   - The list doesn't have any custom fields")
        print("   - The list ID might not exist")
        
except Exception as e:
    print(f"❌ Error while retrieving list and fields: {e}")
    exit(1) 