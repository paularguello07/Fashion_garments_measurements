import argparse
from pathlib import Path
import os
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", type=str, help="Path to the image", default="/Users/paulaarguello/Documents/Fashion_garments_measurements/dataset/Clean_dataset")
args = parser.parse_args()


def optimize_image(image_path, output_path, quality=85):
    # Abrir la imagen
    img = Image.open(image_path)
    
    if img.width > 600 or img.height > 600:
        img.thumbnail((600, 600))

    # Guardar como JPEG con calidad optimizada
    img = img.convert("RGB")  # Convertir a RGB si es PNG
    img.save(output_path, "JPEG", quality=quality)

def main():
    count = 0
    for dress in os.listdir(args.data_path):
        if dress.startswith("dress"):
            name = dress.split("_")[-1]
            image_path = Path(args.data_path) / dress / f"{dress}_irl"

            # Check if the image exists in png, jpg or jpeg format
            if os.path.exists(image_path.with_suffix(".png")) or os.path.exists(image_path.with_suffix(".jpg")) or os.path.exists(image_path.with_suffix(".jpeg")):
                image_path = image_path.with_suffix(".png") if os.path.exists(image_path.with_suffix(".png")) else image_path.with_suffix(".jpg") if os.path.exists(image_path.with_suffix(".jpg")) else image_path.with_suffix(".jpeg")
                output_path = Path(args.data_path) / dress / f"{dress}_irl_lowres.jpg"
                optimize_image(image_path, output_path)
                print(f"Optimized image saved to {output_path}")
                count += 1

    print(f"Optimized {count} images.")

if __name__ == "__main__":
    main()
