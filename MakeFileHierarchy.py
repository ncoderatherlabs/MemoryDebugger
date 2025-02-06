import csv
import json
import sys
from collections import defaultdict

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)

def build_hierarchy(data):
    def nested_dict():
        return defaultdict(nested_dict)
    
    hierarchy = nested_dict()

    for row in data:
        path_parts = row['path'].strip('/').split('/')
        current_level = hierarchy

        for part in path_parts[:-1]:
            current_level = current_level[part]
        
        current_level[path_parts[-1]] = row

    return hierarchy

def write_hierarchy(output_file_path, hierarchy):
    def dicts(tree):
        if isinstance(tree, defaultdict):
            return {k: dicts(v) for k, v in tree.items()}
        return tree

    with open(output_file_path, 'w') as outfile:
        json.dump(dicts(hierarchy), outfile, indent=4, sort_keys=True)

def main(input_file_path, output_file_path):
    data = read_csv(input_file_path)
    hierarchy = build_hierarchy(data)
    write_hierarchy(output_file_path, hierarchy)
    print(f"Hierarchical visualization with row info written to {output_file_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file.csv> <output_file.json>")
    else:
        main(sys.argv[1], sys.argv[2])
