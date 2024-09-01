import argparse
import time
from gemini import Gemini
from pathlib import Path
import os
import json
from google.api_core.exceptions import ResourceExhausted
from validation import generate_content_with_retries
from utils import optimize_image, translate, clean_content
from detect import Detect_a_dress

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help="Path to the image", default="dataset/Clean_dataset")
parser.add_argument("--image", type=str, help="Path to the image", default="dataset/testing/dress1.jpg")
parser.add_argument("--save_path", type=str, help="Path to save json of predictions", default="results/testing")
parser.add_argument("--waist_lenght", type=float, help="CM of the waist", default=75.5)
parser.add_argument("--shoulder_lenght", type=float, help="CM of the shoulder", default=None)
args = parser.parse_args()

print("Starting Testing...")

gemini = Gemini()
detect_dress = Detect_a_dress()
name = args.image.split("/")[-1].split(".")[0]

#create a folder in savepath
args.save_path = args.save_path + "/" + name
if not os.path.exists(args.save_path):
    os.makedirs(args.save_path)

# Detect dress
probas_to_keep, bboxes_scaled, pil_crop_img = detect_dress.run_worflow(args.image, args.save_path)

output_path = args.save_path + "/" + name + "_crop_lowres.jpg"
optimize_image(pil_crop_img, output_path)

image_path = Path(output_path)
results_path = os.path.join(args.save_path, f"{name}_results.json")


content = generate_content_with_retries(image_path)
#content = {"sleeve_width": ["narrow"], "sleeve_length": ["shoulder"], "neck": ["round"], "neckline": ["short"], "skirt_length": ["long"], "skirt_width": ["wide"]}
content = clean_content(content)
content_t = translate(content, spanish_to_english=False)

# Save the results
results = {"content": content}
with open(results_path, "w") as file:
    json.dump(results, file)

my_dress = None
for dress in os.listdir(args.data_path):
    if dress.startswith("dress"):
        attributes = os.path.join(args.data_path, dress, f"{dress}_atributes.txt")
        # open txt
        with open(attributes, "r") as file:
            content_gt = file.read()

        content_gt = content_gt.split("\n")[:-1]

        if content_gt == content_t:
            my_dress = dress
            with open(os.path.join(args.data_path, dress, "skirt_front_distances.txt"), "r") as file:
                distances_skirt = file.read().split("\n")[:-1]
                dist_waist_px = distances_skirt[0].split(":")[1]
                px_to_cm = args.waist_lenght/(2.0*float(dist_waist_px))

            for file in os.listdir(os.path.join(args.data_path, dress)):
                if file.endswith("distances.txt"):
                    with open(os.path.join(args.data_path, dress, file), "r") as txt_file:
                        distances_cms = []
                        distances = txt_file.read().split("\n")[:-1]
                        for dist in distances:
                            dist = dist.split(":")
                            distances_cms.append(float(dist[1])*px_to_cm)

                        #print(f"Distances for {file}: {distances_cms}")
                    #crete new file in save path
                    with open(os.path.join(args.save_path, f"{file}"), "w") as new_file:
                        for dist in distances_cms:
                            new_file.write(f"{dist}\n")
                
                if file.endswith("coordinates.png"):
                    os.system(f"cp {os.path.join(args.data_path, dress, file)} {os.path.join(args.save_path, file)}")
                if file.endswith("uv.png"):
                    os.system(f"cp {os.path.join(args.data_path, dress, file)} {os.path.join(args.save_path, file)}")
            break

print(f"Predicted dress: {my_dress}")
            