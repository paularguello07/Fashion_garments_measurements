from PIL import Image, ImageDraw, ImageFont
import os
import json
from skimage.metrics import structural_similarity as ssim
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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


def find_same_lines(all_lines, all_options, file_names):
    same_lines_full = []
    counter_last = 0 
    for i in range(len(all_options)):
        same_lines = []
        for j in range(len(all_lines)):
            if all_lines[j]== all_options[i]:
                same_lines.append(file_names[j])
        if len(same_lines) > 1:
            counter_last += 1
        same_lines_full.append(same_lines)
    return same_lines_full, counter_last


def etiquetar_manual(new_path, categorias, all_options):
    counter = 0
    all_lines = []
    file_names = []

    for filename in os.listdir(new_path):
        if filename.endswith('.png'):
            txt_filename = filename.replace('.png', '_atributes.txt')
            label = False
            lines = []

            if os.path.exists(os.path.join(new_path, txt_filename)):
                with open(os.path.join(new_path, txt_filename), 'r') as file:
                    lines = file.readlines()
                    all_lines.append(lines)
                    file_names.append(filename)
                    counter += 1
                    #print("Already labeled")
                    #label = False
                    if counter%5 == 0:
                        same_lines, counter_last = find_same_lines(all_lines, all_options, file_names)
                        print("Quedan: ",counter_last)

            if label:
                
                txt_path = os.path.join(new_path, txt_filename)
                img_path = os.path.join(new_path, filename)

                file_names.append(filename)

                # Display the image
                img = Image.open(img_path)
                img.show()
                if counter%5 == 0:
                    same_lines, counter_last = find_same_lines(all_lines, all_options, file_names)
                    print("Quedan: ",counter_last)
                
                        
                # Read the corresponding text file
                
                print("\n -------------------")
                print("Quedan por etiquetar: ",246 - counter)
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
                
    same_lines, counter_last = find_same_lines(all_lines, all_options, file_names)
    return same_lines, counter_last,file_names


def same_lines_counter(samelines):
    counter = 0 
    for i in range(len(same_lines)):
        if len(same_lines[i])>1:
            counter += 1
    return counter

def label_again(new_path, categorias, last_options):
    counter = 0

    for filename in os.listdir(new_path):
        if filename.endswith('.png'):
            txt_filename = filename.replace('.png', '_atributes.txt')
            label = True
            lines = []

            if os.path.exists(os.path.join(new_path, txt_filename)):
                with open(os.path.join(new_path, txt_filename), 'r') as file:
                    lines = file.readlines()
                    counter += 1
                    print("Already labeled")
                    label = False
                    

            if label:
                
                txt_path = os.path.join(new_path, txt_filename)
                img_path = os.path.join(new_path, filename)

                #file_names.append(filename)

                # Display the image
                img = Image.open(img_path)
                img.show()
                
                
                        
                for i in range(len(last_options)):
                    print(i, last_options[i])
                
                option = input("Seleccione una opción: ")
                if option == 'n':
                    os.remove(os.path.join(new_path, img_path))
                else:
                    lines = last_options[int(option)]
                    with open(txt_path, 'w') as file:
                        file.writelines(lines)
                    #all_lines.append(lines)

                    last_options.remove(last_options[int(option)])
                
                img.close()

                counter = counter + 1

new_path = 'P:\Documentos\HDSP\Fashion_garments_measurements\dataset\Paula_dataset_unique'

categorias = {"Ancho de manga": ["Estrecha", "Ancha"], 
              "Largo de manga": ["Sisa", "Al hombro"],
              "Cuello": ["En V", "Redondo"],
              "Escote": ["Corto", "Pronunciado"],
              "Largo de falda": ["Corta", "Larga"], 
              "Ancho de falda": ["Pegada", "Ancha"]}


all_options = find_all_options(categorias)

same_lines, counter_last, file_names = etiquetar_manual(new_path, categorias, all_options)

last_options = []
for i in range(len(same_lines)):
    if same_lines[i] == []:
        last_options.append(all_options[i])


label_again(new_path, categorias, last_options)

"""
for i in range(len(same_lines)):
    if i%5 == 0:
        print("Quedan: ", same_lines_counter(same_lines))

    if same_lines[i] != [] and len(same_lines[i])>1:
        print(all_options[i])

        for j in range(len(same_lines[i])):
            img_path = os.path.join(new_path, same_lines[i][j])
            img = mpimg.imread(img_path)
            #subplots
            plt.subplot(1, len(same_lines[i]), j+1)
            plt.imshow(img)
            plt.axis('off')
            plt.title(j)
        plt.show()

        chosen = input("Choose the correct one: ")
        for j in range(len(same_lines[i])):
            if j != int(chosen):
                
                txt_filename = same_lines[i][j].replace('.png', '_atributes.txt')
                os.remove(os.path.join(new_path, txt_filename))

                
"""



            