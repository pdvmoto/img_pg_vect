
import time as tim
from datetime import datetime, date, time, timezone

from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob, os

# take the filename, to use as prefix for print- and trace-stmnts
pyfile = os.path.basename(__file__)

# ------------------------------------------------
def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp
  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '
  # print ( prfx, ' in function f_prfx: ' , s_prefix )
  return str ( s_prefix )
# end of f_prfx, set sourcefile and timestamp


print ( f_prfx(), '---- starting ---- ' )

size = 128, 128

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    with Image.open(infile) as im:
        im.thumbnail(size)
        im.save(file + "_thumbnail.jpg", "JPEG")

print ( f_prfx(), ' thumbnails done ---------------. ' )

#Load CLIP model
model = SentenceTransformer('clip-ViT-L-14')

print ( f_prfx(), ' Clip model loaded --------------- '  )

#Encode an image:
img_emb = model.encode(Image.open('img1.jpg'))

print ( f_prfx(), ' model.encode image done ---------  ' )

#Encode text descriptions
text_emb = model.encode(['motorcycle', 'river', 'A picture of a motorcycle at a river'])

print ( f_prfx(), ' model.encode text done ---------  ' )

#Compute cosine similarities 
cos_scores = util.cos_sim(img_emb, text_emb)

print ( f_prfx(), ' cos-sim done  ---------  ' )

print(cos_scores)

print ( f_prfx(), ' print scores done  ---------  ' )
