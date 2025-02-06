import os

CATEGORIES = {
    "bluetooth": ["bluetooth", "bt."],
    "wifi": ["wifi", "wl."],
    "camera": ["camera", "cam."],
    "display": ["display", "screen", "lcd"],
    "audio": ["audio", "snd", "sound"],
    "battery": ["battery", "power"],
    "network": ["network", "net", "radio"],
    "nfc": ["nfc"],
    "media": ["media", "audio", "video", "codec"],
    "keystore": ["keystore", "crypto", "secure"],
    "crypto": ["crypto", "encryption", "security"],
    "radio": ["radio", "modem", "rf"],
    "sensor": ["sensor", "accelerometer", "gyroscope"],
    "soc": ["soc", "chip", "processor"],
    "usb": ["usb"],
    "zygote": ["zygote", "dalvik", "runtime"],
    "cne": ["cne"],
    "qc": ["qc", "qualcomm"],
    "value_addons": ["addon", "feature", "extra"],
    "drm": ["drm"],
    "fuse_passthrough": ["fuse", "passthrough"],
    "gatekeeper": ["gatekeeper"],
    "graphics": ["graphics", "sf", "gpu", "display"],
    "general": []
}

def categorize_properties(properties):
    categories = {category: {} for category in CATEGORIES}
    for key, value in properties.items():
        found = False
        for category, keywords in CATEGORIES.items():
            if any(keyword in key.lower() for keyword in keywords):
                categories[category][key] = value
                found = True
                break
        if not found:
            categories["general"][key] = value
    return categories

def extract_properties(file_path):
    properties = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.strip().startswith("#"):
                    key, value = line.split("=", 1)
                    properties[key.strip()] = value.strip()
    except Exception:
        pass
    return properties

def save_to_file(file_name, categorized):
    file_path = f"{file_name}.prop"
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for category, props in categorized.items():
                if props:
                    f.write(f"# {category.replace('_', ' ').title()}\n")
                    for key, value in props.items():
                        f.write(f"{key}={value}\n")
                    f.write("\n")
    except Exception:
        pass

def process_files(root_dir, mapped_files):
    for relative_path, file_name in mapped_files.items():
        file_path = os.path.join(root_dir, relative_path)
        if os.path.exists(file_path):
            properties = extract_properties(file_path)
            if properties:
                categorized = categorize_properties(properties)
                save_to_file(file_name, categorized)

def main():
    root_dir = input("Enter the path to the dump directory: ").strip()
    if not os.path.isdir(root_dir):
        return
    mapped_files = {
        "product/etc/build.prop": "product",
        "system/system/build.prop": "system",
        "system_ext/etc/build.prop": "system_ext",
        "vendor/build.prop": "vendor"
    }
    process_files(root_dir, mapped_files)

if __name__ == "__main__":
    main()
