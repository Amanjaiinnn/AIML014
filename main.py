import sys
import json
from utils.nlp import parse_intent
from openstack_client import (
    create_vm, delete_vm, resize_vm,
    create_volume, delete_volume,create_network,
    get_usage, list_flavors, list_images, list_networks
)

def print_header():
    print("🛰️  Agentic AI - OpenStack Assistant")
    print("====================================")

def get_user_input():
    print("\nEnter your instruction (or 'exit' to quit):")
    return input("> ")

def print_intent_info(result):
    print(f"\n🧾 Detected Intent: {result['intent']}")
    print("🧱 Entities:")
    print(json.dumps(result["entities"], indent=2))


def get_confirmation():
    while True:
        choice = input("\nDo you want to proceed? (yes/no): ").lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def handle_intent(intent, entities):
    try:
        if intent == "create_vm":
            name = entities.get("name", "default-vm")
            flavor_name = entities.get("flavor", "S.4")

            flavor_id = next((f["id"] for f in list_flavors() if f["name"] == flavor_name), None)
            
            image_id = list_images()[0]["id"]
            network_id = list_networks()[0]["id"]

            print(f"name: {name}")
            print(f"flavor_id: {flavor_id}")
            print(f"image_id: {image_id}")
            print(f"network_id: {network_id}")

            if not all([name, flavor_id, image_id, network_id]):
                print("❌ Error: Missing required parameters to create VM.")
            else:
                res = create_vm(name, flavor_id, image_id, network_id)
                print(f"✅ VM created with ID: {res['server']['id']}")

        elif intent == "delete_vm":
            name = entities.get("name")
            res = delete_vm(name)
            print(f"✅ {res}")

        elif intent == "resize_vm":
            name = entities.get("name")
            flavor_name = entities.get("flavor")
            flavor_id = next((f["id"] for f in list_flavors() if f["name"] == flavor_name), None)
            res = resize_vm(name, flavor_id)
            print(f"✅ {res}")

        elif intent == "create_volume":
            name = entities.get("name")
            size = int(entities.get("size", 1))
            res = create_volume(name, size)
            print(f"✅ Volume created: {res['volume']['id']}")

        elif intent == "delete_volume":
            name = entities.get("name")
            res = delete_volume(name)
            print(f"✅ {res}")
        
        elif intent == "create_network":
            name = entities.get("name")
            if not name:
                print("❌ Error: Network name is required.")
            else:
                res = create_network(name)
                print(f"✅ Network created:")
                print(json.dumps(res, indent=2))

        elif intent == "usage":
            usage = get_usage()
            print("\nCurrent Usage:")
            print(json.dumps(usage,indent=2))

        else:
            print("🤖 Unknown intent. Please rephrase your command.")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print_header()
    
    
    while True:
        user_input = get_user_input()
        
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye! 👋")
            sys.exit(0)
        
        if not user_input.strip():
            continue
            
        result = parse_intent(user_input)
        print_intent_info(result)
        
        if result["requires_confirmation"]:
            if get_confirmation():
                handle_intent(result["intent"], result["entities"])
            else:
                print("❌ Operation cancelled by user.")
        else:
            handle_intent(result["intent"], result["entities"])

if __name__ == "__main__":
    main()
