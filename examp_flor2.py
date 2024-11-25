import requests

# note: error on CUDA install.. try later

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM 

filepath='/Users/pdvbv/zz_imgs/91_complex.jpg'
filepath='/Users/pdvbv/zz_imgs/61_surprise_moto.jpg' # OK
filepath='/Users/pdvbv/zz_imgs/8_flowers.jpg'  # OK
filepath='/Users/pdvbv/zz_imgs/2_view.jpg' 

device = "cuda:0" if torch.cuda.is_available() else "cpu"
devide = "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)

prompt = "<OD>"

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"

image = Image.open( filepath )

inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

generated_ids = model.generate(
    input_ids=inputs["input_ids"],
    pixel_values=inputs["pixel_values"],
    max_new_tokens=1024,
    num_beams=3,
    do_sample=False
)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

parsed_answer = processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))

print( 'Parsed answ: ', parsed_answer, '\n\n <---')
print( 'Generated txt: ', parsed_answer, '\n\n <---')
print( ' file was : open ' , filepath )


