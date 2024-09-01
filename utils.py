import argparse
from pathlib import Path
import os
from PIL import Image

categorias = [["Estrecha", "Ancha"], 
              ["Sisa", "Al hombro"],
              ["En V", "Redondo"],
              ["Corto", "Pronunciado"],
              ["Corta", "Larga"], 
              ["Pegada", "Ancha"]]
    
categories = {"sleeve_width": ["narrow", "wide"],
            "sleeve_length": ["armhole", "shoulder"],
            "neck": ["v", "round"],
            "neckline": ["short", "pronounced"],
            "skirt_length": ["short", "long"],
            "skirt_width": ["tight", "wide"]}


def optimize_image(pil_img, output_path, quality=85):
    # Abrir la imagen
    
    if pil_img.width > 600 or pil_img.height > 600:
        pil_img.thumbnail((600, 600))

    # Guardar como JPEG con calidad optimizada
    pil_img = pil_img.convert("RGB")  # Convertir a RGB si es PNG
    pil_img.save(output_path, "JPEG", quality=quality)

def translate(content, spanish_to_english=True):
    # Translate content to categories
    if spanish_to_english:
        content_t = {}
        for idx, i in enumerate(categories):
            index = categorias[idx].index(content[idx])
            content_t[i] = categories[i][index]
    else:
        content_t = []
        for idx, i in enumerate(categories):
            index = categories[i].index(content[i])
            content_t.append(categorias[idx][index])
  
    return content_t

def clean_content(content):
    # Clean the content to get the categories
    for i in content:
        # check if the content is a list
        if type(content[i]) == list:
            content[i] = content[i][0].lower()
        
    return content