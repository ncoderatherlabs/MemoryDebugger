import csv
import sys

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)

def filter_different_resources(file1_data, file2_data):
    file1_paths = {row['path'] for row in file1_data}
    file2_paths = {row['path'] for row in file2_data}
    common_paths = file1_paths.intersection(file2_paths)
    
    different_resources = [row for row in file1_data if not (row['path'] in common_paths)]
    return different_resources

def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(data)

def sort_csv(data):
    return sorted(data, key=lambda row: row['path'])

def main(file1_path, file2_path, output_path):
    file1_data = read_csv(file1_path)
    file2_data = read_csv(file2_path)
    
    different_resources = filter_different_resources(file1_data, file2_data)
    
    if different_resources:
        sorted_different_resources = sort_csv(different_resources)
        write_csv(output_path, sorted_different_resources, fieldnames=file1_data[0].keys())
        print(f"Different texture resources written to {output_path}")
    else:
        print("No different texture resources found.")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1.csv> <file2.csv> <output.csv>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
