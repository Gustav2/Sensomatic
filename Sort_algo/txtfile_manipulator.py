def remove_brackets(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove "[" and "]" from the content
    modified_content = content.replace("[", "").replace("]", "")

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
        
def insert_newlines(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the content by commas
    parts = content.split(',')

    # Insert "\n" after every second comma
    modified_content = ','.join(parts[i] + (',' if i % 2 == 0 else '\n') for i in range(len(parts)))

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
def remove_commas(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process each line
    modified_lines = []
    for line in lines:
        # Remove one comma if there are two commas in a row
        modified_line = line.replace(",,", ",")
        
        # Remove the comma if the line starts with one
        if modified_line.startswith(","):
            modified_line = modified_line[2:]
        
        modified_lines.append(modified_line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

def run(file_path_input):
    file_path = file_path_input

    remove_brackets(file_path)
    insert_newlines(file_path)
    remove_commas(file_path)