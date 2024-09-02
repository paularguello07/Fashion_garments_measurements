
import os 
import json
from utils import translate, clean_content


results_path = "results/validation"
data_path = "dataset/Clean_dataset"
n_results = 0   

full_errors = [0,0,0,0,0,0]
full_accuracy = 0   
def count_errors_parts(content_gt, content_pred):
    errors = [0,0,0,0,0,0]
    for idx, i in enumerate(content_gt):
        if content_gt[i].lower() != content_pred[i].lower():
            errors[idx] = errors[idx] + 1
    return errors


for dress in os.listdir(results_path):
    json_file = os.path.join(results_path, dress, f"{dress}.json")
    name_dress = "dress_sleeveless_" + dress.split("_")[0]
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            results = json.load(file)
            content_pred = results["content"]
            acc = results["accuracy"]
        #print(f"Results for {dress}: {results}")
        n_results += 1

        attributes = os.path.join(data_path, name_dress, f"{name_dress}_atributes.txt")
        # open txt
        with open(attributes, "r") as file:
            content_gt = file.read()

        content_gt_t = translate(content_gt.split("\n")[:-1])
        #print(f"GT: {content_gt_t}")
        #print(f"PR: {clean_content(content_pred)}")
        if acc == 1.0:
            content_pred = content_gt_t
        errors = count_errors_parts(content_gt_t, clean_content(content_pred))
        print(f"Errors: {errors}")
        full_errors = [x + y for x, y in zip(full_errors, errors)]
        accuracy = sum(errors)/len(errors)
        full_accuracy += acc

print(f"Number of results: {n_results}")
print(f"Errors: {full_errors}")
full_errors = [1 - x/n_results for x in full_errors]
part_errors = [0,0,0]
part_errors[0] = full_errors[0] + full_errors[1]
part_errors[1] = full_errors[2] + full_errors[3]
part_errors[2] = full_errors[4] + full_errors[5]
print(f"Part errors: {full_errors}")
print(f"full accuracy: {full_accuracy/n_results}")