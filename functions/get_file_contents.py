import os
from config import MAX_CHARS

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