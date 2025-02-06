import os
import sys
import subprocess

def process_memreports(input_directory):
    # Ensure the directory exists
    if not os.path.isdir(input_directory):
        print(f"Error: The directory '{input_directory}' does not exist.")
        sys.exit(1)
    
    # Iterate over all files in the directory
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)
        # Check if it's a file and has the .memreport extension
        if os.path.isfile(file_path) and filename.lower().endswith('.memreport'):
            print(f"Processing '{filename}'...")
            # Execute MemReportToStats.py on the file
            subprocess.run(['python', 'MemReportToStats.py', file_path])
            subprocess.run(['python', 'MemReportToTextures.py', file_path])
            subprocess.run(['python', 'MakeFileHierarchy.py', file_path.replace('.memreport', '.csv'), file_path.replace('.memreport', '.hierarchy')])
        else:
            print(f"Skipping '{filename}' (not a .memreport file).")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python process_memreports.py <input_directory>")
        sys.exit(1)
    input_directory = sys.argv[1]
    process_memreports(input_directory)
