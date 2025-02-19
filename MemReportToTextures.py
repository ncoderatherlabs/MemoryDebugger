import re
import csv
import os
import argparse

def extract_texture_report(source_file):
    # Check if the file has the .memreport extension
    if not source_file.endswith(".memreport"):
        raise ValueError(f"'{source_file}' does not end with .memreport extension. Please only pass UE4 memreport files!")

    source_file_name = os.path.splitext(os.path.basename(source_file))[0]
    source_file_dir = os.path.dirname(source_file)
    target_file = os.path.join(source_file_dir, f"{source_file_name}.csv")

    # Read the content of the memreport file
    with open(source_file, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # Match the texture report section
    texture_report_match = re.search(r"Listing NONVT textures\.(?P<TextureReport>.*?)Total size:", file_content, re.DOTALL)
    if not texture_report_match:
        raise ValueError("Failed to extract texture report from memreport")

    texture_report = texture_report_match.group("TextureReport")

    # Write the texture report to a CSV file
    with open(target_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        # Write the header
        csv_writer.writerow(["disksize_x", "disksize_y", "disksize_kb", "bias", "memsize_x", "memsize_y", "memsize_kb", "texformat", "texgroup", "path", "bstreaming", "unknown_ref", "vt", "usagecount", "num_mips", "uncompressed"])

        # Split the texture report into lines
        all_lines = texture_report.split('\n')
        for line in all_lines:
            if len(line) == 0:
                continue

            match = re.match(r"(?P<disksize_x>\d+)x(?P<disksize_y>\d+) \((?P<disksize_kb>\d+) KB, (?P<bias>.*?)\), (?P<memsize_x>\d+)x(?P<memsize_y>\d+) \((?P<memsize_kb>\d+) KB\), (?P<texformat>\w+), TEXTUREGROUP_(?P<texgroup>\w+), (?P<path>.*?), (?P<bstreaming>\w+), (?P<unknown_ref>\w+), (?P<vt>\w+), (?P<usagecount>\d+), (?P<num_mips>\d+), (?P<uncompressed>\w+)", line)
            if match:
                csv_writer.writerow([
                    match.group('disksize_x'),
                    match.group('disksize_y'),
                    match.group('disksize_kb'),
                    match.group('bias'),
                    match.group('memsize_x'),
                    match.group('memsize_y'),
                    match.group('memsize_kb'),
                    match.group('texformat'),
                    match.group('texgroup'),
                    match.group('path'),
                    match.group('bstreaming'),
                    match.group('unknown_ref'),
                    match.group('vt'),
                    match.group('usagecount'),
                    match.group('num_mips'),
                    match.group('uncompressed')
                ])
            else:
                print(f"Could not parse line: '{line}'")

    print(f"Saved texture report to {target_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract texture report from UE4 .memreport files and save as CSV.")
    parser.add_argument("source_file", type=str, help="Path to the UE4 memreport file")

    args = parser.parse_args()
    extract_texture_report(args.source_file)
