
from PIL import Image
import torch, torchvision
from torchvision.transforms import functional as F
import matplotlib.pyplot as plt
import torchvision.transforms as T

COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

class Detect_a_dress:
    def __init__(self):
        

        self.finetuned_classes = ['dress',]

        self.transform = T.Compose([
            T.Resize(800),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.model = torch.hub.load('facebookresearch/detr',
                       'detr_resnet50',
                       pretrained=False,
                       num_classes=1)

        checkpoint = torch.load('/Users/paulaarguello/Documents/Fashion_garments_measurements/detection/checkpoint.pth',
                                map_location='cpu')

        self.model.load_state_dict(checkpoint['model'],
                          strict=False)

        self.model.eval()
        
    def filter_bboxes_from_outputs(self, outputs, im,
                                   threshold=0.7):

      # keep only predictions with confidence above threshold
      probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
      keep = probas.max(-1).values > threshold

      probas_to_keep = probas[keep]

      # convert boxes from [0; 1] to image scales
      bboxes_scaled = self.rescale_bboxes(outputs['pred_boxes'][0, keep], im.size)

      return probas_to_keep, bboxes_scaled
    
    def plot_finetuned_results(self, pil_img, save_path, prob=None, boxes=None):
        #plt.figure(figsize=(16,10))
        plt.imshow(pil_img)
        ax = plt.gca()
        colors = COLORS
        if prob is not None and boxes is not None:
            for p, (xmin, ymin, xmax, ymax), c in zip(prob, boxes.tolist(), colors):
                ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                            fill=False, color=c, linewidth=3))
                cl = p.argmax()
                text = f'{self.finetuned_classes[cl]}: {p[cl]:0.2f}'
                ax.text(xmin, ymin, text, fontsize=15,
                        bbox=dict(facecolor='yellow', alpha=0.5))
            plt.axis('off')
            plt.savefig(save_path+'/detection_results.jpg')
        plt.close()


    def box_cxcywh_to_xyxy(self, x):
        x_c, y_c, w, h = x.unbind(1)
        b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
             (x_c + 0.5 * w), (y_c + 0.5 * h)]
        return torch.stack(b, dim=1)


    def rescale_bboxes(self, out_bbox, size):
        img_w, img_h = size
        b = self.box_cxcywh_to_xyxy(out_bbox)
        b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
        return b


    def run_worflow(self, image_path, save_path=None):
      # mean-std normalize the input image (batch-size: 1)
      my_image = Image.open(image_path)
      my_image = my_image.convert('RGB')
      img = self.transform(my_image).unsqueeze(0)

      # propagate through the model
      outputs = self.model(img)


      probas_to_keep, bboxes_scaled = self.filter_bboxes_from_outputs(outputs, my_image,
                                                                    threshold=0.7)
      print(bboxes_scaled)
      xmin, ymin, xmax, ymax = bboxes_scaled.tolist()[0]
      pil_crop_img = my_image.crop((xmin, ymin, xmax, ymax))
      if save_path is not None:
          self.plot_finetuned_results(my_image, save_path, prob=probas_to_keep, boxes=bboxes_scaled)

      return probas_to_keep, bboxes_scaled, pil_crop_img