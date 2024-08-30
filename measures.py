import argparse
import time
from gemini import Gemini
from pathlib import Path
import os
import json
from google.api_core.exceptions import ResourceExhausted


parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help="Path to the image", default="dataset/Clean_dataset")
parser.add_argument("--save_path", type=str, help="Path to save json of predictions", default="results/validation")
args = parser.parse_args()

for dress in os.listdir(args.data_path):
        results = []
        if dress.startswith("dress"):
            # Get the number of the dress
            name = dress.split("_")[-1]
            # Get the path of the image of the dress
            name_path = os.path.join(args.data_path, dress, f"{dress}_irl_lowres.jpg")
            image_path = Path(name_path)