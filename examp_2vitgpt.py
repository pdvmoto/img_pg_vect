
import requests
from PIL import Image
from transformers import ViTFeatureExtractor, AutoTokenizer, FlaxVisionEncoderDecoderModel

loc = "ydshieh/vit-gpt2-coco-en"

feature_extractor = ViTFeatureExtractor.from_pretrained(loc)
tokenizer = AutoTokenizer.from_pretrained(loc)
model = FlaxVisionEncoderDecoderModel.from_pretrained(loc)

# We will verify our results on an image of cute cats
# url = "http://images.cocodataset.org/val2017/000000039769.jpg"

print ( ' ---- main : ---- ' ) 

filepath= str ( '/Users/pdvbv/zz_img/6_room.jpg' ) 

with Image.open( filepath) as img:
    pixel_values = feature_extractor(images=img, return_tensors="np").pixel_values

print ( ' ---- main : pixels extracted ---- ' ) 

def generate_step(pixel_values):

    output_ids = model.generate(pixel_values, max_length=16, num_beams=4).sequences
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]

    return preds

preds = generate_step(pixel_values)

print ( ' ---- predicates : ---- ' ) 

print(preds)

# should produce
# ['a cat laying on top of a couch next to another cat']

