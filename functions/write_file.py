import os
from config import MAX_CHARS
from google.genai import types

def write_file(working_directory, file_path, content):
    new_directory = os.path.join(working_directory, file_path)
    new_directory = os.path.abspath(new_directory)
    new_working_directory = os.path.abspath(working_directory)

    if new_directory.startswith(new_working_directory):
        try:
            if not os.path.exists(new_directory):
                os.makedirs(os.path.dirname(new_directory), exist_ok=True)
            with open(new_directory, "w") as file:
                file.write(content)
            return(f'Successfully wrote to "{new_directory}" ({len(content)} characters written)')
        except Exception as e:
            return f"Error: {e}"
    else:
        return(f'Error: Cannot write to "{new_directory}" as it is outside the permitted working directory')
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the desired file",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the desired file",
            )     
        },
        required=["file_path", "content"]
    ),
)