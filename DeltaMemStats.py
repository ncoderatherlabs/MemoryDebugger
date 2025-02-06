import csv
import sys
import os

def read_stats(file_path):
    stats = {}
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            memory_usage = float(row[0])
            stat_name = row[1]
            stat_group = row[2]
            stat_category = row[3]
            description = row[4]
            stats[stat_name] = (memory_usage, stat_group, stat_category, description)
    return stats

def calculate_deltas(stats1, stats2):
    delta_stats = []
    all_stats = set(stats1.keys()).union(stats2.keys())
    for stat in all_stats:
        usage1 = stats1.get(stat, (0.0, '', '', ''))[0]
        usage2 = stats2.get(stat, (0.0, '', '', ''))[0]
        delta = usage2 - usage1
        stat_group = stats1.get(stat, ('', '', '', ''))[1] or stats2.get(stat, ('', '', '', ''))[1]
        stat_category = stats1.get(stat, ('', '', '', ''))[2] or stats2.get(stat, ('', '', '', ''))[2]
        description = stats1.get(stat, ('', '', '', ''))[3] or stats2.get(stat, ('', '', '', ''))[3]
        delta_stats.append((delta, stat, stat_group, stat_category, description))
    # Sort delta stats by the delta memory usage (high to low)
    delta_stats.sort(key=lambda x: float(x[0]), reverse=True)
    return delta_stats

def write_deltas(delta_stats, output_file_path):
    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Delta Memory Usage (MB)', 'Stat Name', 'STAT Group', 'STAT Category', 'Description'])
        csvwriter.writerows(delta_stats)
    print(f"Delta memory usage stats have been written to {output_file_path}.")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python delta_memory_usage.py <input_stat_file1> <input_stat_file2> <output_file>")
        sys.exit(1)
    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    stats1 = read_stats(input_file1)
    stats2 = read_stats(input_file2)
    delta_stats = calculate_deltas(stats1, stats2)
    write_deltas(delta_stats, output_file)
