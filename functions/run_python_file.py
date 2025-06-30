import os
import subprocess

def run_python_file(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    if not os.path.isdir(working_directory_path):
        return f"Error: Working directory {working_directory} not a directory"
    file_abs_path = os.path.abspath(os.path.join(working_directory_path, file_path))

    if not file_abs_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        process = subprocess.run(
            ["python3", file_abs_path],
            timeout=30,
            capture_output=True
        )
        output = ""
        output += f"STDOUT: {process.stdout.decode()}\n"
        output += f"STDERR: {process.stderr.decode()}\n"
        if process.returncode != 0:
            output += f"Process returned with exit code {process.returncode}"
        if process.stdout.decode() == "":
            output += "No output produced"
        return output
    except Exception as e:
        print(f"Error: executing Python file: {e}")

    