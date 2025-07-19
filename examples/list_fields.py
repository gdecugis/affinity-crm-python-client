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
                    print(f"      📋 Options: {', '.join(options)}")
                else:
                    print(f"      📋 Options: None")
            elif field_type == "number":
                min_val = field.get("min_value")
                max_val = field.get("max_value")
                if min_val is not None or max_val is not None:
                    print(f"      📊 Range: {min_val or 'no min'} to {max_val or 'no max'}")
            
            print()
        
        # Get all possible values for the first field using the correct approach
        if fields:
            first_field = fields[0]
            first_field_id = first_field.get("id")
            first_field_name = first_field.get("name", "Unnamed Field")
            
            print(f"🔍 Getting all possible values for the first field: {first_field_name} (ID: {first_field_id})")
            print()
            
            try:
                # Get field values using the correct endpoint with list_id parameter
                field_values_response = client.list_fields(list_id=LIST_ID)
                
                # The response is a direct array of fields, not wrapped in "fields"
                if field_values_response and isinstance(field_values_response, list):
                    # Find the first field in the response and get its dropdown options
                    for field_data in field_values_response:
                        if field_data.get("id") == first_field_id:
                            dropdown_options = field_data.get("dropdown_options", [])
                            
                            if dropdown_options:
                                print(f"📋 Found {len(dropdown_options)} possible values for field '{first_field_name}':")
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
                            else:
                                print(f"📝 No dropdown options found for field '{first_field_name}'")
                                print("   This field might not be a dropdown type or has no options defined")
                            break
                    else:
                        print(f"❌ Could not find field {first_field_id} in the response")
                else:
                    print(f"📝 No field data received for list {LIST_ID}")
                    
            except Exception as e:
                print(f"❌ Error retrieving values for field '{first_field_name}': {e}")
                print("   This might be because:")
                print("   - The field doesn't have any dropdown options")
                print("   - The field type doesn't support dropdown options")
                print("   - API permissions issue")
    else:
        print(f"📝 No fields found for list {LIST_ID}")
        print("   This could mean:")
        print("   - The list doesn't have any custom fields")
        print("   - The list ID might not exist")
        
except Exception as e:
    print(f"❌ Error while retrieving list and fields: {e}")
    exit(1) 