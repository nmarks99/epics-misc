import re
import sys

def generate_markdown_from_substitutions(file_path):
    """
    Parses an EPICS substitutions file and generates a Markdown table
    of motor names and descriptions, grouped by controller port.

    Args:
        file_path (str): The path to the substitutions file.

    Returns:
        str: A string containing the Markdown-formatted tables.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return f"Error: The file at path '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred while reading the file: {e}"

    # Dictionary to hold motors grouped by their PORT
    motors_by_port = {}

    # Regex to handle quoted strings and commas
    field_pattern = re.compile(r'"[^"]*"|[^,]+')

    # --- First Pass: Find and parse the pattern line ---
    pattern_line_text = None
    pattern_found = False
    for line in lines:
        if "pattern" in line:
            pattern_found = True
            continue
        
        # Check for the header line after the pattern is found
        if pattern_found and line.strip().startswith('{') and line.strip().endswith('}'):
            pattern_line_text = line
            break

    if not pattern_line_text:
        return "Error: Could not find the 'pattern' line or the corresponding header line in the substitutions file."

    # Parse column names from the pattern line
    columns = [field.strip() for field in field_pattern.findall(pattern_line_text.split('{')[1].split('}')[0])]

    try:
        m_index = columns.index('M')
        desc_index = columns.index('DESC')
    except ValueError as e:
        return f"Error: Required column not found in pattern. {e}"

    # --- Second Pass: Process data lines ---
    data_started = False
    for line in lines:
        line = line.strip()

        # Check for the start of the data block
        if not data_started and line.startswith('{') and line.endswith('}'):
            # This is the header line, so we can start processing from the next '{' line
            data_started = True
            continue

        # Process a data line
        if data_started and line.startswith('{'):
            data_fields = [field.strip() for field in field_pattern.findall(line.split('{')[1].split('}')[0])]
            
            # Ensure the line has the correct number of fields
            if len(data_fields) != len(columns):
                continue

            # Get the motor name and description using the found indices
            motor_name_full = data_fields[m_index].replace('"', '')
            desc = data_fields[desc_index].replace('"', '')

            # Determine the port from the motor name
            port = "UNKNOWN_PORT"
            name_parts = motor_name_full.split(':')
            if len(name_parts) >= 2:
                if name_parts[1].startswith('c'):
                    # For patterns like "mcs2:c1:m1"
                    port = f"{name_parts[0]}_{name_parts[1].upper()}"
                elif name_parts[0] and name_parts[1].startswith('m'):
                    # For patterns like "nf:m1"
                    port = name_parts[0].upper()
                else:
                    port = name_parts[0]
            else:
                # For names that don't have a prefix like "nf:m1"
                port = "NO_PORT_PREFIX"
            
            # Add the motor to the dictionary, creating the list for the port if it doesn't exist
            if port not in motors_by_port:
                motors_by_port[port] = []
            
            motors_by_port[port].append({'name': motor_name_full, 'desc': desc})

    # Generate the Markdown table output
    markdown_output = ""
    for port, motors in motors_by_port.items():
        markdown_output += f"### {port}\n"
        markdown_output += "| Motor Name | Description |\n"
        markdown_output += "|---|---|\n"
        for motor in motors:
            markdown_output += f"| {motor['name']} | {motor['desc']} |\n"
        markdown_output += "\n"  # Add a newline for spacing between tables

    return markdown_output

if __name__ == "__main__":
    # Check if a command-line argument was provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_substitutions_file>")
        sys.exit(1)

    # Get the file path from the command-line argument
    file_path_arg = sys.argv[1]

    # Generate and print the markdown
    output = generate_markdown_from_substitutions(file_path_arg)
    print(output)
