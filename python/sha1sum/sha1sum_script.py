import hashlib
import os

def calculate_sha1sum(file_path):
    sha1 = hashlib.sha1()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error calculating SHA-1 for '{file_path}': {e}")
        return None

def update_proprietary_files(file_path, vendor_proprietary_dir):
    updated_lines = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '|' in line:
                    full_path, _ = line.split('|', 1)

                    if ':' in full_path:
                        _, search_path = full_path.split(':', 1)
                    else:
                        search_path = full_path

                    absolute_path = os.path.abspath(os.path.join(vendor_proprietary_dir, search_path))

                    if os.path.isfile(absolute_path):
                        sha1sum = calculate_sha1sum(absolute_path)
                        if sha1sum:
                            updated_lines.append(f"{full_path}|{sha1sum}")
                            print(f"Updated: {full_path}|{sha1sum}")
                        else:
                            updated_lines.append(line)
                    else:
                        print(f"File not found: {search_path}")
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)

        with open(file_path, 'w') as f:
            f.write('\n'.join(updated_lines) + '\n')
        print(f"File '{file_path}' successfully updated.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"Error updating '{file_path}': {e}")

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    device_name = os.path.basename(base_path)
    vendor_proprietary_path = os.path.abspath(os.path.join(base_path, "../../../vendor/samsung", device_name, "proprietary"))

    proprietary_files_path = os.path.join(base_path, "proprietary-files.txt")
    
    print(f"Device: {device_name}")
    print(f"Vendor/proprietary directory: {vendor_proprietary_path}")
    
    update_proprietary_files(proprietary_files_path, vendor_proprietary_path)

if __name__ == "__main__":
    main()
