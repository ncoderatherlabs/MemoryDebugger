import csv
import sys
import os

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)

def read_asset_list(file_path):
    with open(file_path, newline='') as csvfile:
        return [line.strip() for line in csvfile]

def normalize_path(path):
    base_name = os.path.basename(path)
    if '.' in base_name:
        path = path[:path.rfind('.')]
    return path

def filter_assets(first_file_data, second_file_assets):
    assets_in_both = []
    assets_in_first_not_in_second = []

    second_file_assets_set = set(second_file_assets)

    for row in second_file_assets_set:
        print(row)

    for row in first_file_data:
        path = row['path']
        path = normalize_path(path)
        print(path) 
        if path in second_file_assets_set:
            assets_in_both.append(row)
        else:
            assets_in_first_not_in_second.append(row)

    return assets_in_both, assets_in_first_not_in_second

def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(data)

def sort_csv(data):
    return sorted(data, key=lambda row: row['path'])

def main(first_file_path, second_file_path, output_file_path_1, output_file_path_2):
    first_file_data = read_csv(first_file_path)
    second_file_assets = read_asset_list(second_file_path)

    assets_in_both, assets_in_first_not_in_second = filter_assets(first_file_data, second_file_assets)
    
    if assets_in_both:
        sorted_assets_in_both = sort_csv(assets_in_both)
        write_csv(output_file_path_1, sorted_assets_in_both, fieldnames=first_file_data[0].keys())
        print(f"Assets existing in both files written to {output_file_path_1}")
    else:
        print("No assets found in both files.")

    if assets_in_first_not_in_second:
        sorted_assets_in_first_not_in_second = sort_csv(assets_in_first_not_in_second)
        write_csv(output_file_path_2, sorted_assets_in_first_not_in_second, fieldnames=first_file_data[0].keys())
        print(f"Assets existing in the first file but not in the second file written to {output_file_path_2}")
    else:
        print("No assets found only in the first file.")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python script.py <first_file.csv> <second_file.txt> <output_file_1.csv> <output_file_2.csv>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
