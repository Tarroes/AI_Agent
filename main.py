import os
import sys
from dotenv import load_dotenv
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

print(f"API Key loaded: {api_key is not None}")

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def main():
    if len(sys.argv) == 1:
        print("Error: No input")
        sys.exit(1)
    else:
        user = sys.argv[1]
        messages = [types.Content(role="user", parts =[types.Part(text=user)]),
]
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        
        if "--verbose" in sys.argv:
            print(f"User prompt: {user}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if hasattr(response, 'function_calls') and response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            call_function()

if __name__ == "__main__":
    main()
