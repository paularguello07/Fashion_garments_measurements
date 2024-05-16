from PIL import Image, ImageDraw, ImageFont
import os
import json
from skimage.metrics import structural_similarity as ssim
import numpy as np


def find_same_lines(all_lines, lines):
    for line in all_lines:
        if line == lines:
            return True
    return False

new_path = 'P:\Documentos\HDSP\Fashion_garments_measurements\dataset\Paula_dataset_unique'

categorias = [{"Ancho de manga": ["Estrecha", "Ancha"]}, 
              {"Largo de manga": ["Sisa", "Al hombro"]},
              {"Cuello": ["En V", "Redondo"]},
              {"Escote": ["Corto", "Pronunciado"]},
              {"Largo de falda": ["Corta", "Larga"]}, 
              {"Ancho de falda": ["Pegada", "Ancha"]}]

counter = 0

all_lines = []
unique_lines = []
for filename in os.listdir(new_path):
    if filename.endswith('.png'):
        txt_filename = filename.replace('.png', '_atributes.txt')
        label = True
        lines = []

        if os.path.exists(os.path.join(new_path, txt_filename)):
            with open(os.path.join(new_path, txt_filename), 'r') as file:
                lines = file.readlines()
                all_lines.append(lines)
                counter += 1
                print("Already labeled")
                label = False


        if label:
               
            txt_path = os.path.join(new_path, txt_filename)
            img_path = os.path.join(new_path, filename)

            # Display the image
            img = Image.open(img_path)
            img.show()

            # Read the corresponding text file
            
            print("\n -------------------")
            print("Quedan por etiquetar: ",167 - counter)
            print("\n")
            
            for value in categorias:
                for key, values in value.items():
                    print(key)
                    print("1. ", values[0])
                    print("2. ", values[1])
                    option = input("Seleccione una opción: ")
                    lines.append(values[int(option)-1] + '\n')

            with open(txt_path, 'w') as file:
                file.writelines(lines)
            
            all_lines.append(lines)

            counter = counter + 1
        