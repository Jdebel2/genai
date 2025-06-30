import os

def write_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory_path):
        return f"Error: Working directory {working_directory} not a directory"
    file_abs_path = os.path.abspath(os.path.join(working_directory_path, file_path))

    if not file_abs_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(working_directory_path):
        os.makedirs(working_directory_path)

    try:
        with open(file_abs_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")
    
