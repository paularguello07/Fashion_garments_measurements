import argparse
import time
from gemini import Gemini
from pathlib import Path
import os
import json
from google.api_core.exceptions import ResourceExhausted
from detect import Detect_a_dress
from utils import optimize_image
from utils import translate, clean_content


gemini = Gemini()
detect_dress = Detect_a_dress()

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help="Path to the image", default="dataset/Clean_dataset")
parser.add_argument("--save_path", type=str, help="Path to save json of predictions", default="results/validation")
args = parser.parse_args()


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
        best_acc = 0
        if dress.startswith("dress"):
            # Get the number of the dress
            name = dress.split("_")[-1]
            # Get the path of the image of the dress
            name_path_org = Path(args.data_path) / dress / f"{dress}_irl"
            low_res_path = Path(args.data_path) / dress / f"{dress}_irl_lowres.jpg"
            name_low_res_path = args.data_path +"/"+ dress +"/"+ f"{dress}_irl_lowres.jpg"
            #image_path = Path(name_path)

            if os.path.exists(name_path_org.with_suffix(".png")) or os.path.exists(name_path_org.with_suffix(".jpg")) or os.path.exists(name_path_org.with_suffix(".jpeg")):
                name_path_org = name_path_org.with_suffix(".png") if os.path.exists(name_path_org.with_suffix(".png")) else name_path_org.with_suffix(".jpg") if os.path.exists(name_path_org.with_suffix(".jpg")) else name_path_org.with_suffix(".jpeg")
             
                predict = False
                json_results_path = os.path.join(args.save_path, name+"_results" , f"{name}_results.json")
                results_path = os.path.join(args.save_path, name+"_results")
                # search if the results exists
                if os.path.exists(json_results_path):
                    with open(json_results_path, "r") as file:
                        results = json.load(file)
                    if results["accuracy"] < 0.6: # if the accuracy is less than 1, predict again
                        predict = True
                        print(f"Predicting again for {name}")
                    else: # if the accuracy is 1, add to the accuracy
                        n_val = n_val + 1
                        best_acc = results["accuracy"]
                        acc = acc + best_acc
                        predict = False
                        print(f"Found results for {name} with accuracy {best_acc}")
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
                    if not os.path.exists(results_path):
                        os.makedirs(results_path)

                    try:
                        # Detect dress
                        probas_to_keep, bboxes_scaled, pil_crop_img = detect_dress.run_worflow(name_path_org, results_path)
                        optimize_image(pil_crop_img, low_res_path)
                        image_path = Path(low_res_path)
                    except Exception as e: 
                        print(f"Failed to detect dress for {name}: {e}")
                        continue

                    try:
                        content = generate_content_with_retries(image_path)
                        content = clean_content(content)
                        n_val = n_val + 1
                    except Exception as e:
                        print(f"Failed to generate content for {name}: {e}")
                        continue

                    print(content)
                    print(content_gt_t)

                    acc_ind = accuracy(content_gt_t, content)
                    if acc_ind > best_acc:
                        best_acc = acc_ind

                    print(f"Accuracy: {best_acc}")
                    print("-------------------------------------------------")

                    acc = acc + best_acc

                    #save content to json
                    results = {"image": name_low_res_path, "content": content, "accuracy": best_acc}
                    with open(json_results_path, "w") as file:
                        json.dump(results, file)

    print(f"Accuracy: {acc/n_val}")


if __name__ == "__main__":
    main(args)