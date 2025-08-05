import os
import subprocess
from config import MAX_CHARS
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    new_directory = os.path.join(working_directory, file_path)
    new_directory = os.path.abspath(new_directory)
    new_working_directory = os.path.abspath(working_directory)

    if new_directory.startswith(new_working_directory):
        try:
            if not os.path.exists(new_directory):
                return(f'Error: File "{file_path}" not found.')
            if not file_path.endswith(".py"):
                return(f'Error: "{file_path}" is not a Python file.')
            process_list = ["python", new_directory] + args
            completed_process =subprocess.run(process_list,capture_output=True,timeout = 30,cwd=new_working_directory)
            output_string = ""
            if completed_process.stdout != (b''):
                output_string += f"STDOUT: {completed_process.stdout.decode('utf-8')}\n"
            if completed_process.stderr != (b''):
                output_string += f"STDERR: {completed_process.stderr.decode('utf-8')}\n"
            if completed_process.returncode != 0:
                output_string += f"Process exited with code {completed_process.returncode}"
            if output_string == "":
                return("No output produced.")
            return output_string
        except Exception as e:
            return f"Error: executing Python file: {e}"
    else:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file. If file is not python, returns an error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the desired file",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The arguments to be passed along to the target python file",
            ),
        },
        required=["file_path"]
    ),
)