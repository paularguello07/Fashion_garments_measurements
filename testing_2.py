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
parser.add_argument("--image", type=str, help="Path to the image", default="dataset/testing/dress6.png")
parser.add_argument("--save_path", type=str, help="Path to save json of predictions", default="results/testing")
parser.add_argument("--waist_lenght", type=float, help="CM of the waist", default=75.5)
parser.add_argument("--shoulder_lenght", type=float, help="CM of the shoulder", default=None)
args = parser.parse_args()

print("Starting Testing...")

name = args.image.split("/")[-1].split(".")[0]
args.save_path = os.path.join(args.save_path, name)
results_path = os.path.join(args.save_path, f"{name}_results.json")

#read content from results_path
if os.path.exists(results_path):
    with open(results_path, "r") as file:
        results = json.load(file)
        content = results["content"]

content_t = clean_content(content)
content_t = translate(content_t, spanish_to_english=False)

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
            for file in os.listdir(os.path.join(args.data_path, dress)):
                #print(file)
                if file.endswith("_uv.png"):
                    os.system(f"cp {os.path.join(args.data_path, dress, file)} {os.path.join(args.save_path, file)}")
            break

print(f"Predicted dress: {my_dress}")
            