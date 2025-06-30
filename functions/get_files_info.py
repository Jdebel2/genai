import os

def get_files_info(working_directory, directory=None):
    working_directory_path = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory_path):
        return f"Error: Working directory {working_directory} not a directory"
    directory_path = os.path.abspath(os.path.join(working_directory_path, directory))

    if not directory_path.startswith(working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.abspath(directory_path)):
        return f'Error: "{directory}" is not a directory'
    
    try:
        file_info = []
        for file in os.listdir(os.path.abspath(directory_path)):
            file_path = os.path.abspath(f"{directory_path}/{file}")
            file_info.append(f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}")
        output = "\n".join(file_info)
        return output
    except Exception as e:
        return f"Error: {e}"