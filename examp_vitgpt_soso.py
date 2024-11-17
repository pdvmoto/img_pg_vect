
from transformers import AutoImageProcessor, ViTForImageClassification
import torch
from PIL import Image

import requests

filepath= str ( '/Users/pdvbv/zz_imgs/6_motorcycle.jpg' )

img = Image.open( filepath)

image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

inputs = image_processor(img, return_tensors="pt")

with torch.no_grad():
    logits = model(**inputs).logits

# model predicts one of the 1000 ImageNet classes
predicted_label = logits.argmax(-1).item()
print(model.config.id2label[predicted_label])
