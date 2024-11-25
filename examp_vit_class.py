from transformers import AutoImageProcessor, FlaxViTForImageClassification
from PIL import Image
import jax
import requests

fullpath = "/Users/pdvbv/zz_imgs/1_udine.jpg" 
image = Image.open( fullpath )

image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = FlaxViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

inputs = image_processor(images=image, return_tensors="np")
outputs = model(**inputs)
logits = outputs.logits

# model predicts one of the 1000 ImageNet classes
predicted_class_idx = jax.numpy.argmax(logits, axis=-1)
print("Predicted class:", model.config.id2label[predicted_class_idx.item()])


for n_idx in range ( len ( model.config.id2label ) ):
  print (  "..  ", n_idx, model.config.id2label [ n_idx ]  )

print ( ' --- done ---- ')

