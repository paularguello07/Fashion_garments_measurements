"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
from pathlib import Path
import os
import textwrap
import json

genai.configure(api_key="AIzaSyANRiFo79Q-pr5dgqNM-ElLPzaj0a7RWmg")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 1024,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel("gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

image_path = Path("images/image1.jpeg")
image_part = {
    "mime_type": "image/jpeg",
    "data": image_path.read_bytes()
}


prompt_parts = [
    textwrap.dedent("""\
    Describe the dress
      If your sleeve width is wide or narrow,
       If your sleeve length is armhole sleeve or shoulder length sleeve,
       If your neck is round or V, 
       If your neckline is short or pronounced,
       If your skirt length is long or short,
       If your skirt width is wide skirt or tight skirt. With a json format
    {"sleeve width": str, "sleeve length": str, "neck": str, "neckline": str, "skirt length": str, "skirt width": str}
    """),
    image_part
]
response = model.generate_content(prompt_parts)
data = json.loads(response.text) 
print(json.dumps(data))


