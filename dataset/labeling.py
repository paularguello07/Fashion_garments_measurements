from PIL import Image, ImageDraw, ImageFont
import os
import json
from skimage.metrics import structural_similarity as ssim
import numpy as np

def find_all_options(categorias):
    all_options = []

    for i in categorias['Ancho de manga']:
        for j in categorias['Largo de manga']:
            for k in categorias['Cuello']:
                for l in categorias['Escote']:
                    for m in categorias['Largo de falda']:
                        for n in categorias['Ancho de falda']:
                            option= [i+"\n", j+"\n", k+"\n", l+"\n", m+"\n", n+"\n"]
                            all_options.append(option)
    return all_options


def find_same_lines(all_lines, all_options):
    same_lines_full = []
    counter_last = 0 
    for i in range(len(all_options)):
        same_lines = []
        for j in range(len(all_lines)):
            if all_lines[j]== all_options[i]:
                same_lines.append(j)
        if same_lines == []:
            counter_last += 1
        same_lines_full.append(same_lines)
    return same_lines_full, counter_last


def etiquetar_manual(new_path, categorias, all_options):
    counter = 0
    all_lines = []

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
                if counter%5 == 0:
                    same_lines, counter_last = find_same_lines(all_lines, all_options)
                    print("Quedan: ",counter_last)
                
                        
                # Read the corresponding text file
                
                print("\n -------------------")
                print("Quedan por etiquetar: ",167 - counter)
                print("\n")
                

                for values in categorias.items():
                    print(values[0])
                    print("1. ", values[1][0])
                    print("2. ", values[1][1])
                    option = input("Seleccione una opción: ")
                    lines.append(values[1][int(option)-1] + '\n')

                with open(txt_path, 'w') as file:
                    file.writelines(lines)
                
                all_lines.append(lines)

                counter = counter + 1
                
    same_lines, counter_last = find_same_lines(all_lines, all_options)
    return same_lines, counter_last




new_path = '/Users/paulaarguello/Documents/Fashion_garments_measurements/dataset/Paula_dataset_unique'

categorias = {"Ancho de manga": ["Estrecha", "Ancha"], 
              "Largo de manga": ["Sisa", "Al hombro"],
              "Cuello": ["En V", "Redondo"],
              "Escote": ["Corto", "Pronunciado"],
              "Largo de falda": ["Corta", "Larga"], 
              "Ancho de falda": ["Pegada", "Ancha"]}


all_options = find_all_options(categorias)

same_lines, counter_last = etiquetar_manual(new_path, categorias, all_options)

for i in range(len(same_lines)):
    if same_lines[i] == []:
        print(all_options[i])



            