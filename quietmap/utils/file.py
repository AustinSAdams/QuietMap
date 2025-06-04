import os
import json
import sys
from colorama import Fore, Style

API_KEYS_DIR = "quietmap/api"
API_KEYS_FILENAME = "keys.json"
API_KEYS_FILE_PATH = os.path.join(API_KEYS_DIR, API_KEYS_FILENAME)

def load_all_keys():
    if not os.path.exists(API_KEYS_FILE_PATH):
        return {}
    try:
        with open(API_KEYS_FILE_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (IOError, json.JSONDecodeError) as e:
        print(f"{Fore.YELLOW}[WARNING]: Could not read or parse {API_KEYS_FILE_PATH}. Starting with empty keys. {Style.RESET_ALL}\n{Fore.RED}[ERROR]: {e}")
        return {}

def save_all_keys(keys_data):
    os.makedirs(API_KEYS_DIR, exist_ok=True)
    try:
        with open(API_KEYS_FILE_PATH, 'w') as f:
            json.dump(keys_data, f, indent=4)
    except IOError as e:
        print(f"{Fore.RED}[ERROR] saving API keys to {API_KEYS_FILE_PATH}: {e}")

def get_api_key(service_name):
    keys = load_all_keys()
    return keys.get(service_name)

def add_or_update_api_key(service_name, key_value):
    keys_data = load_all_keys()
    keys_data[service_name] = key_value.strip()
    save_all_keys(keys_data)
    print(f"{Fore.GREEN}[LOG] API key for '{service_name}' successfully written to {API_KEYS_FILE_PATH}")

def list_keys_logic(service_name=None):
    keys = load_all_keys()
    if not keys:
        print(f"{Fore.YELLOW}[WARNING] No API keys found.")
        print(f"Use '{Fore.BLUE}quietmap add_key <service_name> <key_value>{Style.RESET_ALL}'")
        return
    if service_name:
        if service_name in keys:
            key = keys[service_name]
            print(f"{Fore.CYAN}--- Stored API Keys ---")
            print(f"{service_name}:{key}")
            print(f"{Fore.CYAN}-----------------------")
    else:
        print(f"{Fore.CYAN}--- Stored API Keys ---")
        for service, key in keys.items():
            print(f"{service}:{key}")
        print(f"{Fore.CYAN}-----------------------")

def delete_api_key(service_name):
    keys = load_all_keys()
    if service_name in keys:
        del keys[service_name]
        save_all_keys(keys)
        print(f"{Fore.GREEN}[LOG] '{service_name}' API key deleted.")
    else:
        print(f"{Fore.RED}[ERROR] No API key found for '{service_name}'.")

def clear_all_api_keys():
    save_all_keys({})
    print(f"{Fore.GREEN}[LOG] All API keys have been successfully removed.")

def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            print(f"[ERROR] Cannot make output directory!\n\nError: {e}")
            sys.exit(1)
    else:
        pass
