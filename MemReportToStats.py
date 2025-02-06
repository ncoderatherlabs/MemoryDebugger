import re
import csv
import sys
import os

def parse_memreport(input_file_path):
    # Strictly check for '.memreport' extension
    base, ext = os.path.splitext(input_file_path)
    if ext.lower() != '.memreport':
        print("Error: The input file does not have a '.memreport' extension.")
        sys.exit(1)
    else:
        output_csv_path = base + '.stats.csv'

    # Regular expression to match memory usage lines with additional columns, including negative values
    memory_usage_pattern = re.compile(
        r'^\s*([-+]?\d*\.?\d+)\s*MB\s*-\s*(.*?)\s*-\s*(.*?)\s*-\s*(.*?)\s*-\s*(.*)$',
        re.MULTILINE
    )

    stats = []

    with open(input_file_path, 'r') as file:
        lines = file.readlines()
        start_parsing = False
        for line in lines:
            if start_parsing:
                match = memory_usage_pattern.match(line)
                if match:
                    memory_value = match.group(1).strip()
                    stat_name = match.group(2).strip()
                    stat_group = match.group(3).strip()
                    stat_category = match.group(4).strip()
                    description = match.group(5).strip()
                    stats.append((memory_value, stat_name, stat_group, stat_category, description))
                else:
                    break
            if "AssetRegistry memory usage = " in line:
                start_parsing = True

    # Sort delta stats by the delta memory usage (high to low)
    stats.sort(key=lambda x: float(x[0]), reverse=True)

    # Write the extracted stats to a CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Memory Usage (MB)', 'Stat Name', 'STAT Group', 'STAT Category', 'Description'])
        csvwriter.writerows(stats)

    print(f"Memory usage stats have been written to {output_csv_path}.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python parse_memreport.py <input_memreport_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    parse_memreport(input_file)
