import google.generativeai as genai
from pathlib import Path
import os
import textwrap
import json
from PIL import Image


class Gemini:
    def __init__(self):
        # Set up the API key
         
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

        self.model = genai.GenerativeModel("gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        
        self.prompt_parts = [
            textwrap.dedent("""\
            {"sleeve_width": "wide/narrow", "sleeve_length": "armhole/shoulder", "neck": "round/V", "neckline": "short/pronounced", "skirt_length": "long/short", "skirt_width": "wide/tight"}
            """)
        ]
        
    def generate_content(self, image_path):

        image_path = Path(image_path)
        image_part = {
            "mime_type": "image/jpg",
            "data": image_path.read_bytes()
        }
        
        prompt = self.prompt_parts + [image_part]
        
        response = self.model.generate_content(prompt)
        #print(response.usage_metadata)
        data = json.loads(response.text)
        
        return data
