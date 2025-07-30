import os
import sys
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)

print(f"API Key loaded: {api_key is not None}")

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
        )
        if "--verbose" in sys.argv:
            print(f"User prompt: {user}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("Hello from ai-agent!")
        print(response.text)

if __name__ == "__main__":
    main()
