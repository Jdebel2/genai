import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def main():
    model_name = 'gemini-2.0-flash-001'
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    mode_verbose = False


    if len(sys.argv) > 1 and (sys.argv[1] != '--verbose' and sys.argv[1] != '-v'):
        prompt = sys.argv[1]
    else:
        sys.exit(1)

    if '--verbose' in sys.argv or '-v' in sys.argv:
        mode_verbose = True


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]


    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Read file contents in the specified file_path, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to read file contents from, relative to the working directory.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write or overwrite files, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to read file contents from, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file",
                )
            }
        )
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Execute Python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to execute Python file with optional arguments from, relative to the working directory.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name, contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    num_calls = 0
    while num_calls <= 20:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part, mode_verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Fatal: program doesn't work")
            print(f"-> {function_call_result.parts[0].function_response.response}")
            num_calls += 1
            if num_calls <= 20:
                break
        
        variations = response.candidates
        n_messages = []
        for v in variations:
            n_messages = v.content
        messages.extend(n_messages)
        response = client.models.generate_content(
            model=model_name, contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
    
    print(response.text)
    if mode_verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    args = function_call_part.args.copy()
    args["working_directory"] = './calculator'

    
    function_result = None
    match function_call_part.name:
        case "get_files_info":
            function_result = get_files_info(**args)
        case "get_file_content":
            function_result = get_file_content(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case "write_file":
            function_result = write_file(**args)
    
    if "Error" in function_result:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


main()



