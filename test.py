import google.generativeai as genai
from google.api_core import exceptions

print("Gemini SDK working!")

# You can catch errors like this:
try:
    raise exceptions.ResourceExhausted("Quota exceeded")
except exceptions.ResourceExhausted as e:
    print("Caught:", e)
