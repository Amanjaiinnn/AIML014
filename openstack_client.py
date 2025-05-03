import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("OS_PROJECT_ID")
password=os.getenv("OS_PASSWORD")
username=os.getenv("OS_USERNAME")
auth_url=os.getenv("OS_AUTH_URL")

def get_openstack_token():
    
    url = f"{auth_url}/auth/tokens"

    body = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": username,
                        "domain": {"id": "default"},
                        "password": password
                    }
                }
            },
            "scope": {
                "project": {
                    "id": PROJECT_ID
                }
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 201:
        raise Exception(f"Authentication failed: {response.status_code} {response.text}")

    token = response.headers.get("X-Subject-Token")
    

    return token


def get_headers():
    return {
        "Content-Type": "application/json",
        "X-Auth-Token": get_openstack_token()
    }


COMPUTE_URL = f"https://api-ap-south-mum-1.openstack.acecloudhosting.com:8774/v2.1/{PROJECT_ID}"
NETWORK_URL = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:9696"
VOLUME_URL = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:8776/v3"
USAGE_URL = f"{COMPUTE_URL}/os-simple-tenant-usage/{PROJECT_ID}"


def list_flavors():
    r = requests.get(f"{COMPUTE_URL}/flavors/detail", headers=get_headers())
    return r.json().get("flavors", [])


def list_images():
    r = requests.get("https://api-ap-south-mum-1.openstack.acecloudhosting.com:9292/v2/images", headers=get_headers())
    return r.json().get("images", [])


def list_networks():
    r = requests.get(f"{NETWORK_URL}/v2.0/networks", headers=get_headers())
    return r.json().get("networks", [])

def create_vm(name, flavor_id, image_id, network_id):
    url = f"{COMPUTE_URL}/servers"
    
    # Get the selected flavor to check its disk size
    flavors = list_flavors()
    flavor = next((f for f in flavors if f["id"] == flavor_id), None)
    if not flavor:
        raise Exception("❌ Flavor not found")

    # If disk == 0, use volume-backed boot
    if flavor["disk"] == 0:
        print("📦 Using volume-backed boot since flavor has 0 disk")

        # Create a bootable volume from the image
        volume_size = 20  # You might want to make this configurable or dynamic
        volume_payload = {
            "volume": {
                "size": volume_size,
                "name": f"{name}-boot-vol",
                "imageRef": image_id
            }
        }

        volume_res = requests.post(
            f"{VOLUME_URL}/{PROJECT_ID}/volumes",
            headers=get_headers(),
            json=volume_payload
        )
        volume_res.raise_for_status()
        volume = volume_res.json()["volume"]
        volume_id = volume["id"]
        print(f"⏳ Creating bootable volume: {volume_id}")

        # Wait for volume to become available
        import time
        for _ in range(10):  # 10 attempts, 5 sec each = 50 sec max
            status_check = requests.get(
                f"{VOLUME_URL}/{PROJECT_ID}/volumes/{volume_id}",
                headers=get_headers()
            )
            status = status_check.json()["volume"]["status"]
            if status == "available":
                break
            print(f"⏳ Waiting for volume to be ready (status: {status})...")
            time.sleep(5)
        else:
            raise Exception("❌ Volume did not become available in time")

        # Launch VM using volume
        payload = {
            "server": {
                "name": name,
                "flavorRef": flavor_id,
                "networks": [{"uuid": network_id}],
                "block_device_mapping_v2": [{
                    "boot_index": 0,
                    "uuid": volume_id,
                    "source_type": "volume",
                    "destination_type": "volume",
                    "delete_on_termination": True
                }]
            }
        }

    else:
        print("🖼️ Using image-backed boot since flavor has disk > 0")

        # Launch VM using image directly
        payload = {
            "server": {
                "name": name,
                "imageRef": image_id,
                "flavorRef": flavor_id,
                "networks": [{"uuid": network_id}]
            }
        }

    # Create the VM
    r = requests.post(url, headers=get_headers(), json=payload)
    r.raise_for_status()
    return r.json()


#this is the delete vm function

def delete_vm(name):
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
    server = next((s for s in servers if s["name"] == name), None)
    if not server:
        raise Exception(f"No VM named {name} found")
    r = requests.delete(f"{COMPUTE_URL}/servers/{server['id']}", headers=get_headers())
    r.raise_for_status()
    return f"Deleted VM: {name}"


def toggle_vm_status(name, action):
    valid_actions = {
        "start": "os-start",
        "stop": "os-stop",
        "pause": "pause",
        "unpause": "unpause",
        "suspend": "suspend",
        "resume": "resume"
    }

    if action not in valid_actions:
        raise ValueError("❌ Invalid action. Must be one of: start, stop, pause, unpause, suspend, resume")

    # Find the VM by name
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
    server = next((s for s in servers if s["name"] == name), None)
    if not server:
        raise Exception(f"❌ No VM named '{name}' found")

    server_id = server["id"]
    payload = {valid_actions[action]: None}
    r = requests.post(f"{COMPUTE_URL}/servers/{server_id}/action", headers=get_headers(), json=payload)
    r.raise_for_status()

    return f"✅ Action '{action}' performed on VM: {name}"

def resize_vm(name, flavor_id):
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
    server = next((s for s in servers if s["name"] == name), None)
    if not server:
        raise Exception(f"❌ No VM named '{name}' found")

    server_id = server["id"]
    server_details = requests.get(f"{COMPUTE_URL}/servers/{server_id}", headers=get_headers()).json()["server"]

    # Detect volume-backed VM
    is_volume_backed = server_details.get("image") is None
    if is_volume_backed:
        raise Exception("❌ Resize not supported: Volume-backed VMs cannot be resized directly via API. Please recreate the VM with the desired flavor.")

    # Ensure VM is SHUTOFF
    toggle_vm_status("dev-box", "stop")
    if server_details.get("status") != "SHUTOFF":
        raise Exception(f"❌ VM must be SHUTOFF before resizing (current status: {server_details.get('status')})")

    payload = {
        "resize": {
            "flavorRef": flavor_id
        }
    }
    r = requests.post(f"{COMPUTE_URL}/servers/{server_id}/action", headers=get_headers(), json=payload)
    r.raise_for_status()
    return f"✅ Resize initiated for VM: {name}"



def create_volume(name, size):
    payload = {
        "volume": {
            "size": size,
            "name": name
        }
    }
    r = requests.post(f"{VOLUME_URL}/{PROJECT_ID}/volumes", headers=get_headers(), json=payload)
    r.raise_for_status()
    return r.json()


def delete_volume(name):
    r = requests.get(f"{VOLUME_URL}/{PROJECT_ID}/volumes", headers=get_headers())
    volumes = r.json()["volumes"]
    vol = next((v for v in volumes if v["name"] == name), None)
    if not vol:
        raise Exception(f"No volume named {name} found")
    r = requests.delete(f"{VOLUME_URL}/{PROJECT_ID}/volumes/{vol['id']}", headers=get_headers())
    r.raise_for_status()
    return f"Deleted Volume: {name}"

def create_network(name, cidr="192.168.0.0/24", ip_version=4):
    headers = get_headers()

    # 1. Create the network
    network_payload = {
        "network": {
            "name": name,
            "admin_state_up": True
        }
    }
    net_res = requests.post(f"{NETWORK_URL}/v2.0/networks", headers=headers, json=network_payload)
    net_res.raise_for_status()
    network = net_res.json()["network"]

    # 2. Create the subnet for this network
    subnet_payload = {
        "subnet": {
            "name": f"{name}-subnet",
            "network_id": network["id"],
            "ip_version": ip_version,
            "cidr": cidr,
            "enable_dhcp": True
        }
    }
    subnet_res = requests.post(f"{NETWORK_URL}/v2.0/subnets", headers=headers, json=subnet_payload)
    subnet_res.raise_for_status()
    subnet = subnet_res.json()["subnet"]

    # 3. Return combined details
    return {
        "network_id": network["id"],
        "network_name": network["name"],
        "subnet_id": subnet["id"],
        "subnet_name": subnet["name"],
        "cidr": subnet["cidr"]
    }

def get_usage():
    r = requests.get(USAGE_URL, headers=get_headers())
    r.raise_for_status()
    usage_data= r.json()["tenant_usage"]
    usage_data.pop("server_usages",None)
    return usage_data



def get_project_usage_summary():
    headers = get_headers()

    # 1. Get basic usage (vCPUs, RAM)
    
    usage_data = get_usage()["tenant_usage"]

   
    total_vcpus = usage_data.get("total_vcpus_usage", 0)
    total_ram_mb = usage_data.get("total_memory_mb_usage", 0)
    

    # 2. Get GPU count from active flavors used by current servers
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=headers).json()["servers"]
    flavor_ids = {s["flavor"]["id"] for s in servers}
    gpu_count = 0

    for flavor_id in flavor_ids:
        extra_resp = requests.get(f"{COMPUTE_URL}/flavors/{flavor_id}/os-extra_specs", headers=headers)
        if extra_resp.status_code == 200:
            specs = extra_resp.json().get("extra_specs", {})
            gpu_count += int(specs.get("accel:gpu_count", 0))

    # 3. Get total volume usage
    volumes = requests.get(f"{VOLUME_URL}/{PROJECT_ID}/volumes", headers=headers).json()["volumes"]
    total_volume_gb = sum(v["size"] for v in volumes if v["status"] != "deleted")

    # 4. Return formatted summary
    return {
        "vCPUs used": round(total_vcpus, 2),
        "RAM used (MB)": round(total_ram_mb, 2),
        "GPUs used": gpu_count,
        "Total Volume (GB)": total_volume_gb
    }



