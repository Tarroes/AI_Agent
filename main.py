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
    verbose_enabled = False
    if len(sys.argv) == 1:
        print("Error: No input")
        sys.exit(1)
    else:
        user = sys.argv[1]
        messages = [types.Content(role="user", parts =[types.Part(text=user)]),
]
        try:
            countdown = 20
            while countdown > 0:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
            )

        
                if "--verbose" in sys.argv:
                    verbose_enabled = True
                    print(f"User prompt: {user}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
                has_function_calls = False

                for candidate in response.candidates:
                    messages.append(candidate.content)
    
                    if candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                has_function_calls = True

                                function_storage = call_function(part.function_call, verbose_enabled)
                
                                if verbose_enabled and function_storage.parts[0].function_response.response:
                                    print(f"-> {function_storage.parts[0].function_response.response}")
                
                                messages.append(function_storage)
                        
                if not has_function_calls and response.text:
                    print("Final response:")
                    print(response.text)
                    break
                else:
                    countdown -= 1
        except Exception as e:
            return f"Error: {e}"
        
        

if __name__ == "__main__":
    main()
