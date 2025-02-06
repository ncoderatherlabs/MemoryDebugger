import json
import sys

def calculate_sizes(hierarchy):
    total_memsize_kb = 0
    total_disksize_kb = 0

    def traverse_hierarchy(node):
        nonlocal total_memsize_kb, total_disksize_kb
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, dict):
                    traverse_hierarchy(value)
                elif isinstance(value, str):
                    if key == 'memsize_kb':
                        total_memsize_kb += int(value)
                    elif key == 'disksize_kb':
                        total_disksize_kb += int(value)
        else:
            for item in node:
                traverse_hierarchy(item)

    traverse_hierarchy(hierarchy)
    return total_memsize_kb, total_disksize_kb

def main(hierarchy_file_path):
    with open(hierarchy_file_path, 'r') as infile:
        hierarchy = json.load(infile)

    total_memsize_kb, total_disksize_kb = calculate_sizes(hierarchy)
    print(f"Total memsize_kb: {total_memsize_kb}")
    print(f"Total disksize_kb: {total_disksize_kb}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <hierarchy_file.json>")
    else:
        main(sys.argv[1])
