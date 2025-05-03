# # # import os
# # # import requests
# # # from dotenv import load_dotenv

# # # load_dotenv()

# # # AUTH_URL = os.getenv("OS_AUTH_URL")
# # # USERNAME = os.getenv("OS_USERNAME")
# # # PASSWORD = os.getenv("OS_PASSWORD")
# # # PROJECT_NAME = os.getenv("OS_PROJECT_NAME")
# # # USER_DOMAIN = os.getenv("OS_USER_DOMAIN_NAME")
# # # PROJECT_DOMAIN = os.getenv("OS_PROJECT_DOMAIN_NAME")

# # # def get_token():
# # #     url = f"{AUTH_URL}/v3/auth/tokens"
# # #     data = {
# # #         "auth": {
# # #             "identity": {
# # #                 "methods": ["password"],
# # #                 "password": {
# # #                     "user": {
# # #                         "name": USERNAME,
# # #                         "domain": {"name": USER_DOMAIN},
# # #                         "password": PASSWORD
# # #                     }
# # #                 }
# # #             },
# # #             "scope": {
# # #                 "project": {
# # #                     "name": PROJECT_NAME,
# # #                     "domain": {"name": PROJECT_DOMAIN}
# # #                 }
# # #             }
# # #         }
# # #     }
# # #     headers = {"Content-Type": "application/json"}
# # #     res = requests.post(url, json=data, headers=headers)
# # #     return res.headers["X-Subject-Token"], res.json()

# # # def create_vm(name, flavor):
# # #     token, _ = get_token()
# # #     compute_url = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:8774/v2.1/servers"
# # #     body = {
# # #         "server": {
# # #             "name": name,
# # #             "imageRef": "your-image-id",
# # #             "flavorRef": flavor,
# # #             "networks": [{"uuid": "your-network-id"}]
# # #         }
# # #     }
# # #     headers = {"X-Auth-Token": token, "Content-Type": "application/json"}
# # #     res = requests.post(compute_url, json=body, headers=headers)
# # #     return res.json()

# # # Add similar stubs for resize_vm(), delete_vm(), create_network(), create_volume(), etc.

# # # openstack_client.py

# # import requests
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # # ENV vars
# # AUTH_URL = os.getenv("OS_AUTH_URL")
# # USERNAME = os.getenv("OS_USERNAME")
# # PASSWORD = os.getenv("OS_PASSWORD")
# # PROJECT_NAME = os.getenv("OS_PROJECT_NAME")
# # USER_DOMAIN_NAME = os.getenv("OS_USER_DOMAIN_NAME", "Default")
# # PROJECT_DOMAIN_NAME = os.getenv("OS_PROJECT_DOMAIN_NAME", "Default")
# # COMPUTE_URL = os.getenv("OS_COMPUTE_URL")  # Example: https://...:8774/v2.1

# # # def authenticate():
# # #     """Authenticate and return the auth token and project ID."""
# # #     url = f"{AUTH_URL}/auth/tokens"
# # #     headers = {"Content-Type": "application/json"}
# # #     body = {
# # #         "auth": {
# # #             "identity": {
# # #                 "methods": ["password"],
# # #                 "password": {
# # #                     "user": {
# # #                         "name": USERNAME,
# # #                         "domain": {"name": USER_DOMAIN_NAME},
# # #                         "password": PASSWORD
# # #                     }
# # #                 }
# # #             },
# # #             "scope": {
# # #                 "project": {
# # #                     "name": PROJECT_NAME,
# # #                     "domain": {"name": PROJECT_DOMAIN_NAME}
# # #                 }
# # #             }
# # #         }
# # #     }

# #     # res = requests.post(url, headers=headers, json=body)
# #     # res.raise_for_status()

# #     # token = res.headers.get("X-Subject-Token")
# #     # project_id = res.json()["token"]["project"]["id"]

# #     # return token, project_id

# # def create_vm(name, flavor):
# #     """Create a VM with given name and flavor."""
# #     token= gAAAAABoFb_47N166hTtOUN622_Xf3tFSFodtA21KmJ6GV55x7XNfLeIOFhotU8zuc-C1DonkFyYktJ_xCfZe09VoRbaprCi4wjVHohXyrlgUa31FVisK-mBhBfse-CBLKA9B4gwOgKwC3147d6R-IDjz5apecGYgvnTUOYGuWZ_srUvTeY0VTg
# #     # ,
# #     # project_id = authenticate()

# #     url = f"{COMPUTE_URL}/servers"
# #     headers = {
# #     "X-Auth-Token": os.getenv("OS_AUTH_TOKEN"),
# #     "Content-Type": "application/json"
# # }

    
# #     # You may need to adjust imageRef and network UUIDs per your setup
# #     server_data = {
# #         "server": {
# #             "name": name,
# #             "imageRef": "your-image-id-here",  # Replace with actual image ID
# #             "flavorRef": flavor,
# #             "networks": [{"uuid": "your-network-id-here"}],  # Replace with actual network UUID
# #         }
# #     }

# #     res = requests.post(url, headers=headers, json=server_data)
# #     res.raise_for_status()
# #     return res.json()

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# AUTH_TOKEN = os.getenv("OS_AUTH_TOKEN")
# PROJECT_ID = os.getenv("OS_PROJECT_ID")

# COMPUTE_URL = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:8774/v2.1"
# NETWORK_URL = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:9696"
# IMAGE_URL = "https://api-ap-south-mum-1.openstack.acecloudhosting.com:9292"
# FLAVOR_URL = COMPUTE_URL + "/flavors"

# get_headers() = {
#     "X-Auth-Token": AUTH_TOKEN,
#     "Content-Type": "application/json"
# }

# def list_images():
#     response = requests.get(f"{IMAGE_URL}/v2/images", headers=get_headers())
#     return response.json().get("images", [])

# def list_flavors():
#     response = requests.get(f"{FLAVOR_URL}", headers=get_headers())
#     return response.json().get("flavors", [])

# def list_networks():
#     response = requests.get(f"{NETWORK_URL}/v2.0/networks", headers=get_headers())
#     return response.json().get("networks", [])

# def create_vm(name, flavor_id, image_id, network_id):
#     url = f"{COMPUTE_URL}/servers"
#     payload = {
#         "server": {
#             "name": name,
#             "imageRef": image_id,
#             "flavorRef": flavor_id,
#             "networks": [{"uuid": network_id}]
#         }
#     }
#     response = requests.post(url, headers=get_headers(), json=payload)
#     if response.status_code in [200, 202]:
#         return response.json()
#     else:
#         raise Exception(f"Failed to create VM: {response.text}")

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("OS_AUTH_TOKEN")
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
    # catalog = response.json().get("token", {}).get("catalog", [])

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


# def create_vm(name, flavor_id, image_id, network_id):
#     url = f"{COMPUTE_URL}/servers"
#     payload = {
#         "server": {
#             "name": name,
#             "imageRef": image_id,
#             "flavorRef": flavor_id,
#             "networks": [{"uuid": network_id}]
#         }
#     }
#     r = requests.post(url, headers=get_headers(), json=payload)
#     try:
#         r.raise_for_status()
#         return r.json()
#     except requests.exceptions.HTTPError as e:
#         print(f"❌ HTTP Error: {r.status_code} - {r.text}")
#         raise
#     except ValueError:
#         print(f"❌ Invalid JSON response: {r.text}")
#         raise

    # print(image_id)
    # print(flavor_id)
    # r = requests.post(url, headers=get_headers(), json=payload)
    # r.raise_for_status()
    

    # return r.json()


def delete_vm(name):
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
    server = next((s for s in servers if s["name"] == name), None)
    if not server:
        raise Exception(f"No VM named {name} found")
    r = requests.delete(f"{COMPUTE_URL}/servers/{server['id']}", headers=get_headers())
    r.raise_for_status()
    return f"Deleted VM: {name}"


# def resize_vm(name, flavor_id):
#     servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
#     server = next((s for s in servers if s["name"] == name), None)
#     if not server:
#         raise Exception(f"No VM named {name} found")
#     payload = {
#         "resize": {
#             "flavorRef": flavor_id
#         }
#     }
#     r = requests.post(f"{COMPUTE_URL}/servers/{server['id']}/action", headers=get_headers(), json=payload)
#     r.raise_for_status()
#     return f"Resized VM: {name}"

def resize_vm(name, flavor_id):
    # Get all servers
    servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=get_headers()).json()["servers"]
    server = next((s for s in servers if s["name"] == name), None)
    if not server:
        raise Exception(f"❌ No VM named '{name}' found")

    server_id = server["id"]

    # Fetch detailed server info to check root device (volume-backed)
    server_details = requests.get(f"{COMPUTE_URL}/servers/{server_id}", headers=get_headers()).json()["server"]

    # Check if VM is volume-backed (root device is not an ephemeral disk)
    is_volume_backed = "block_device_mapping_v2" in server_details or server_details.get("OS-EXT-SRV-ATTR:root_device_name", "").startswith("/dev/")
    if is_volume_backed:
        raise Exception("❌ Resize not supported: Volume-backed VMs cannot be resized directly via API on this setup. Please recreate the VM with the desired flavor.")

    # Proceed with resize for eligible VMs
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

    # usage_data = usage.get("tenant_usage", {})
    total_vcpus = usage_data.get("total_vcpus_usage", 0)
    total_ram_mb = usage_data.get("total_memory_mb_usage", 0)
    # total_vcpus = usage_data["total_vcpus_usage"]
    # total_ram_mb = usage_data["total_memory_mb_usage"]

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



# def get_project_usage_summary():
#     headers = get_headers()

#     usage_data = get_usage()["tenant_usage"]
#     total_vcpus = usage_data["total_vcpus_usage"]
#     total_ram_mb = usage_data["total_memory_mb_usage"]

#     # Get unique flavors used by active servers
#     servers = requests.get(f"{COMPUTE_URL}/servers/detail", headers=headers).json()["servers"]
#     flavor_ids = {s["flavor"]["id"] for s in servers}
    
#     gpu_count = 0
#     for flavor_id in flavor_ids:
#         r = requests.get(f"{COMPUTE_URL}/flavors/{flavor_id}/os-extra_specs", headers=headers)
#         if r.status_code == 200:
#             specs = r.json().get("extra_specs", {})
#             gpu_count += int(specs.get("accel:gpu_count", 0))

#     # Get total active volume size
#     volumes = requests.get(f"{VOLUME_URL}/{PROJECT_ID}/volumes", headers=headers).json()["volumes"]
#     total_volume_gb = sum(v["size"] for v in volumes if v["status"] != "deleted")

#     # Format and return a clean summary
#     summary = (
#         f"📊 **Project Usage Summary**\n"
#         f"• vCPUs: {round(total_vcpus, 2)}\n"
#         f"• RAM: {round(total_ram_mb, 2)} MB\n"
#         f"• GPUs: {gpu_count}\n"
#         f"• Volumes: {total_volume_gb} GB"
#     )
#     return summary
