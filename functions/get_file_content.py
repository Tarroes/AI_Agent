import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    new_directory = os.path.join(working_directory, file_path)
    new_directory = os.path.abspath(new_directory)
    new_working_directory = os.path.abspath(working_directory)

    if new_directory.startswith(new_working_directory):
        if os.path.isfile(new_directory):
            try:
                with open(new_directory, "r") as f:
                    content = f.read(MAX_CHARS + 1)
                    if len(content) > MAX_CHARS:
                        return content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    else:
                        return content
            except Exception as e:
                return f"Error: {e}"
        else:
            return(f'Error: File not found or is not a regular file: "{file_path}"')
    else:
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Access the content of the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the desired file",
            ),
        },
        required=["file_path"]
    ),
)