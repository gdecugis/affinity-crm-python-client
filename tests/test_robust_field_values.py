#!/usr/bin/env python3
"""
Test script to demonstrate the improved robust field values functionality.
This shows how the new entity_type parameter and auto-detection work.
"""

from affinity.client import AffinityClient
import os

def test_robust_field_values():
    """Test the improved list_field_values and set_field_value methods."""
    
    # Initialize client (you'll need to set your API key)
    api_key = os.getenv('AFFINITY_API_KEY')
    if not api_key:
        print("Please set AFFINITY_API_KEY environment variable")
        return
    
    client = AffinityClient(api_key)
    
    print("Testing improved field values functionality...")
    
    # Example 1: Explicit entity type (most reliable)
    print("\n1. Testing with explicit entity_type=1 (organization):")
    try:
        # Replace with actual organization ID from your Affinity instance
        org_id = 123  # Replace with real organization ID
        result = client.list_field_values(org_id, entity_type=1, field_id=456)
        print(f"✅ Successfully listed field values for organization {org_id}")
        print(f"   Found {len(result.get('field_values', []))} field values")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Example 2: Auto-detection (tries each entity type)
    print("\n2. Testing with auto-detection:")
    try:
        # Replace with actual entity ID from your Affinity instance
        entity_id = 456  # Replace with real entity ID
        result = client.list_field_values(entity_id, field_id=789)
        print(f"✅ Successfully auto-detected entity type for ID {entity_id}")
        print(f"   Found {len(result.get('field_values', []))} field values")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Example 3: Smart set_field_value with explicit entity type
    print("\n3. Testing set_field_value with explicit entity_type:")
    try:
        # Replace with actual IDs from your Affinity instance
        field_id = 123
        entity_id = 456
        value = "Test Value"
        
        result = client.set_field_value(field_id, value, entity_id, entity_type=1)
        print(f"✅ Successfully set field value for organization {entity_id}")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Example 4: Smart set_field_value with auto-detection
    print("\n4. Testing set_field_value with auto-detection:")
    try:
        # Replace with actual IDs from your Affinity instance
        field_id = 789
        entity_id = 101
        value = "Auto-detected Test Value"
        
        result = client.set_field_value(field_id, value, entity_id)
        print(f"✅ Successfully set field value with auto-detection for ID {entity_id}")
        print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    test_robust_field_values()
