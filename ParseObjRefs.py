import re
import sys
import json
from typing import Dict, List, Optional

# Classes for Objects and References (unchanged)
class ObjectNode:
    def __init__(self, object_id: str):
        self.object_id = object_id
        self.references: List[Reference] = []
        self.attributes = {}

    def to_dict(self):
        return {
            'object_id': self.object_id,
            'references': [ref.to_dict() for ref in self.references],
            'attributes': self.attributes
        }

class Reference:
    def __init__(self, member_name: str, from_object_id: str, to_object_id: str):
        self.member_name = member_name
        self.from_object_id = from_object_id
        self.to_object_id = to_object_id
        self.attributes = {}

    def to_dict(self):
        return {
            'member_name': self.member_name,
            'from_object_id': self.from_object_id,
            'to_object_id': self.to_object_id,
            'attributes': self.attributes
        }

# Data structures (unchanged)
objects: Dict[str, ObjectNode] = {}
stacks: List[List[Reference]] = []
current_stack: List[Reference] = []

# Regular expressions to parse the log lines
timestamp_regex = r'^\[\d{4}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}:\d{3}\]\[\d+\]\s*'
arrow_line_regex = re.compile(
    timestamp_regex + r'([->^]+)\s*(.*)'
)
reference_line_regex = re.compile(
    timestamp_regex + r'(.*?)\s*=\s*(\w+)\s+(.*)'
)
root_node_regex = re.compile(
    timestamp_regex + r'(?:\([^\)]*\)\s*)?(.*)'
)

# Function to check if a line represents a function (now refined)
def is_function_reference(content: str) -> bool:
    # Check if content contains a function signature
    # Function signatures often end with '::FunctionName(' or 'FunctionName('
    function_pattern = r'(?:\w+::)?\w+\s*\(.*\)'
    if re.search(function_pattern, content):
        return True
    else:
        return False

# Function to extract object ID and member name from a line
def extract_reference(line: str) -> Optional[Reference]:
    # Remove timestamp for simplicity
    line_content = re.sub(timestamp_regex, '', line)
    if is_function_reference(line_content):
        return None  # Skip function references

    # Match assignment lines
    match = re.match(r'(.*?)\s*=\s*(\w+)\s+(.*)', line_content)
    if match:
        member_info = match.group(1).strip()
        object_type = match.group(2).strip()
        object_path = match.group(3).strip()

        # The object ID is the object path
        object_id = object_path

        # Member name is extracted properly, even if it contains '::'
        member_name = member_info

        # Return a Reference instance
        return Reference(member_name=member_name, from_object_id='', to_object_id=object_id)
    else:
        # Could not extract a reference
        return None

def extract_object_id(content: str) -> Optional[str]:
    if is_function_reference(content):
        return None  # Skip function references

    # Attempt to extract object path after object type
    match = re.match(r'(?:[\w<>]+\s+)?(\/[^\s]+)', content)
    if match:
        object_id = match.group(1).strip()
        return object_id
    else:
        return None

def process_line(line):
    global current_stack

    line = line.strip()
    if not line:
        return

    # Remove timestamp for simplicity
    line_content = re.sub(timestamp_regex, '', line)

    # First, check if the line represents a function reference
    if is_function_reference(line_content):
        return  # Skip function references

    # Try to extract a reference line
    reference = extract_reference(line)
    if reference:
        # Add object if not already added
        if reference.to_object_id not in objects:
            objects[reference.to_object_id] = ObjectNode(object_id=reference.to_object_id)

        # Set from_object_id based on current stack
        if current_stack:
            previous_reference = current_stack[-1]
            reference.from_object_id = previous_reference.to_object_id
        else:
            reference.from_object_id = ''  # No parent

        # Add reference to object
        objects[reference.to_object_id].references.append(reference)
        current_stack.append(reference)
    else:
        # Match arrow lines
        arrow_match = arrow_line_regex.match(line)
        if arrow_match:
            arrow_type = arrow_match.group(1).strip()
            content = arrow_match.group(2).strip()

            object_id = extract_object_id(content)
            if object_id:
                # Add object if not already added
                if object_id not in objects:
                    objects[object_id] = ObjectNode(object_id=object_id)

                # Create a reference from previous object to current object
                if current_stack:
                    previous_reference = current_stack[-1]
                    parent_object_id = previous_reference.to_object_id
                    reference = Reference(member_name='', from_object_id=parent_object_id, to_object_id=object_id)
                    objects[object_id].references.append(reference)
                    current_stack.append(reference)
                else:
                    # No parent object; start a new stack
                    reference = Reference(member_name='', from_object_id='', to_object_id=object_id)
                    objects[object_id].references.append(reference)
                    current_stack.append(reference)
            else:
                # Unable to extract object ID
                pass
        else:
            # Match root node lines
            root_match = root_node_regex.match(line)
            if root_match:
                content = root_match.group(1).strip()

                object_id = extract_object_id(content)
                if object_id:
                    # Start a new stack
                    if current_stack:
                        stacks.append(current_stack)
                    current_stack = []

                    # Add object if not already added
                    if object_id not in objects:
                        objects[object_id] = ObjectNode(object_id=object_id)
                    # No parent in root node
                    previous_object_id = None

                    # Create a reference for the root object
                    reference = Reference(member_name='', from_object_id='', to_object_id=object_id)
                    objects[object_id].references.append(reference)
                    current_stack.append(reference)
                else:
                    # Unable to extract object ID
                    pass
            else:
                # Line didn't match any expected patterns; skip
                pass

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <log_file> <output_json_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        with open(log_file, 'r') as file:
            for line in file:
                process_line(line)

        # Add the last stack if not empty
        if current_stack:
            stacks.append(current_stack)

        # Prepare data for JSON serialization
        data = {
            'objects': {object_id: obj_node.to_dict() for object_id, obj_node in objects.items()},
            'stacks': [
                [ref.to_dict() for ref in stack]
                for stack in stacks
            ]
        }

        # Write to JSON file
        with open(output_file, 'w') as out_file:
            json.dump(data, out_file, indent=4)

        print(f"Data structures have been written to {output_file}")

    except FileNotFoundError:
        print(f"File not found: {log_file}")
        sys.exit(1)

if __name__ == "__main__":
    main()
