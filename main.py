import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

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


client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
print(response.text)
if mode_verbose:
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")