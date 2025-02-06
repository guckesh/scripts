import os

def remove_duplicates_preserve_spacing(file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            seen = set()
            result = []

            for line in lines:
                stripped_line = line.strip()
                if stripped_line == "" or stripped_line.startswith("#"):
                    result.append(line)
                elif line not in seen:
                    seen.add(line)
                    result.append(line)

            with open(file_path, 'w') as file:
                file.writelines(result)

            print(f"Duplicates successfully removed from the file '{file_path}'.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred while processing the file '{file_path}': {e}")

file_paths = ['proprietary-files.txt']

remove_duplicates_preserve_spacing(file_paths)
