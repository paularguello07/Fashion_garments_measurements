import argparse
import time
from gemini import Gemini
from pathlib import Path
import os
import json
from google.api_core.exceptions import ResourceExhausted


categorias = [["Estrecha", "Ancha"], 
              ["Sisa", "Al hombro"],
              ["En V", "Redondo"],
              ["Corto", "Pronunciado"],
              ["Corta", "Larga"], 
              ["Pegada", "Ancha"]]
    
categories = {"sleeve_width": ["narrow", "wide"],
            "sleeve_length": ["armhole", "shoulder"],
            "neck": ["V", "round"],
            "neckline": ["short", "pronounced"],
            "skirt_length": ["short", "long"],
            "skirt_width": ["tight", "wide"]}

gemini = Gemini()


parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help="Path to the image", default="dataset/Clean_dataset")
parser.add_argument("--save_path", type=str, help="Path to save json of predictions", default="results/validation")
args = parser.parse_args()

def translate(content, spanish_to_english=True):
    # Translate content to categories
    if spanish_to_english:
        content_t = {}
        for idx, i in enumerate(categories):
            index = categorias[idx].index(content[idx])
            content_t[i] = categories[i][index]
    else:
        content_t = []
        for i in content:
            index = categories[i].index(content[i])
            content_t.append(categorias[i][index])
  
    return content_t

def clean_content(content):
    # Clean the content to get the categories
    for i in content:
        # check if the content is a list
        if type(content[i]) == list:
            content[i] = content[i][0]
        
    return content


def accuracy(content_gt, content):
    # Calculate accuracy of the prediction
    a = 0
    for i in content_gt:
        if content_gt[i].lower() == content[i].lower():
            a = a + 1
    accuracy = a/len(content_gt)
    return accuracy

def generate_content_with_retries(image_path, max_retries=5, initial_delay=4):
    retries = 0
    delay = initial_delay
    
    while retries < max_retries:
        try:
            # Try to generate content with the image
            content = gemini.generate_content(image_path)
            return content
        except ResourceExhausted as e:
            #print(f"Resource exhausted: {e}. Retry {retries + 1}/{max_retries} in {delay} seconds.")
            time.sleep(delay)
            retries += 1
            delay *= 2  # Exponential backoff

    raise Exception(f"Max retries exceeded. Could not generate content for {image_path}.")

            
def main(args):
    acc = 0
    n_val = 0
    
    for dress in os.listdir(args.data_path):
        results = []
        if dress.startswith("dress"):
            # Get the number of the dress
            name = dress.split("_")[-1]
            # Get the path of the image of the dress
            name_path = os.path.join(args.data_path, dress, f"{dress}_irl_lowres.jpg")
            image_path = Path(name_path)

            if image_path.exists():
                predict = False
                results_path = os.path.join(args.save_path, f"{name}_results.json")
                # search if the results exists
                if os.path.exists(results_path):
                    with open(results_path, "r") as file:
                        results = json.load(file)
                    if results["accuracy"] < 1.0: # if the accuracy is less than 1, predict again
                        predict = True
                        print(f"Predicting again for {image_path}")
                    elif results["accuracy"] == 1.0: # if the accuracy is 1, add to the accuracy
                        n_val = n_val + 1
                        acc = acc + 1.0
                        predict = False
                        print(f"Found results for {image_path} with accuracy 1.0 :)")
                else: # if the results does not exists, predict
                    predict = True
                        
                if predict: 
                    # Get gt attributes of the dress
                    attributes = os.path.join(args.data_path, dress, f"{dress}_atributes.txt")
                    # open txt
                    with open(attributes, "r") as file:
                        content_gt = file.read()

                    content_gt_t = translate(content_gt.split("\n")[:-1])
                    
                    # Generate content with retries
                    try:
                        content = generate_content_with_retries(image_path)
                        content = clean_content(content)
                        n_val = n_val + 1
                    except Exception as e:
                        print(f"Failed to generate content for {image_path}: {e}")
                        continue

                    print(content)
                    print(content_gt_t)
                    acc_ind = accuracy(content_gt_t, content)
                    print(f"Accuracy: {acc_ind}")
                    print("-------------------------------------------------")

                    acc = acc + acc_ind

                    #save content to json
                    results = {"image": name_path, "content": content, "accuracy": acc_ind}
                    with open(results_path, "w") as file:
                        json.dump(results, file)

    print(f"Accuracy: {acc/n_val}")


if __name__ == "__main__":
    main(args)