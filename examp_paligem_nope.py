
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import requests
import torch

print ( ' --- start - ' )
model_id = "gokaygokay/paligemma-rich-captions"

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"

img_file="/Users/pdvbv/zz_imgs/91_complex.jpg"

print ( ' --- opening image  - ' )

image = Image.open( img_file )

model = PaliGemmaForConditionalGeneration.from_pretrained(model_id)
processor = AutoProcessor.from_pretrained(model_id)

print ( ' --- image, model, process defined - ' )

## prefix
prompt = "caption en"
model_inputs = processor(text=prompt, images=image, return_tensors="pt")

print ( ' --- inputs received - ' )

input_len = model_inputs["input_ids"].shape[-1]


with torch.inference_mode():

    print ( ' --- inside while  - ' )
    generation = model.generate(**model_inputs, max_new_tokens=256, do_sample=False)
    generation = generation[0][input_len:]
    decoded = processor.decode(generation, skip_special_tokens=True)
    print(decoded)

