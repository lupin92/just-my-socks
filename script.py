import base64
import requests
import json

# List of URLs
urls = [
    "https://justmysocks3.net/members/getsub.php?service=55534&id=cc8c177d-7a9e-444c-86b4-a1fc90b1fbee&usedomains=1&noss=1",
    "https://justmysocks3.net/members/getsub.php?service=388138&id=827aa158-679f-4c5e-8a84-d8f7d142c9de&usedomains=1&noss=1",
    "https://justmysocks3.net/members/getsub.php?service=463251&id=3f405ae0-e4f6-4ab5-8ca9-0bfe0717ed86&usedomains=1&noss=1",
    "https://justmysocks3.net/members/getsub.php?service=406623&id=a9fe9666-3dfd-444c-8b01-1b1e48478c53&usedomains=1&noss=1"
]

# Mapping of files
file_names = ["us.txt", "jp.txt", "nl.txt", "us2.txt"]

def fix_base64_padding(data):
    """Add padding to Base64 strings if needed."""
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    return data

def process_vmess_data(data):
    """Process the vmess data and return formatted lines."""
    decoded_data = base64.b64decode(data).decode('utf-8')
    entries = decoded_data.split('\n')
    formatted_entries = []
    
    for entry in entries:
        if entry.startswith('vmess://'):
            vmess_data = entry[8:]  # Remove 'vmess://'
            try:
                # Fix Base64 padding if necessary
                vmess_data = fix_base64_padding(vmess_data)
                json_data = base64.b64decode(vmess_data).decode('utf-8')
                json_obj = json.loads(json_data)
                
                ps = json_obj.get("ps", "unknown")
                add = json_obj.get("add", "unknown")
                port = json_obj.get("port", "unknown")
                id = json_obj.get("id", "unknown")
                
                formatted_entry = f"{ps} = vmess, {add}, {port}, username={id}"
                formatted_entries.append(formatted_entry)
            except Exception as e:
                print(f"Failed to process entry: {entry[:100]}... Error: {e}")
    
    return formatted_entries

def main():
    all_entries = []
    
    # Download and process each URL
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Process each vmess data section in the response
            entries = process_vmess_data(response.text)
            all_entries.extend(entries)
        except Exception as e:
            print(f"Failed to download or process {url}. Error: {e}")
    
    # Write the entries to files
    for file_name, entries in zip(file_names, [all_entries[i::4] for i in range(4)]):
        with open(file_name, 'w') as f:
            for entry in entries:
                f.write(entry + '\n')

if __name__ == "__main__":
    main()
