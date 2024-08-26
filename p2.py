# this is result from chatgpt.. "how to store vectors in datbase"


# pip install psycopg2


# the python code...

import os
import time as tim
from datetime import datetime, date, time, timezone

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import psycopg2


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

# Load the pre-trained ResNet50 model without the final classification layer (include_top=False)
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

def extract_vector(img_path):
    """
    Extract feature vector from an image using ResNet50.
    
    :param img_path: Path to the image file.
    :return: Feature vector as a numpy array.
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    vector = features.flatten()
    return vector

def store_vector_in_db(image_name, vector, conn):
    """
    Store feature vector in PostgreSQL database.
    
    :param image_name: Name of the image file.
    :param vector: Feature vector as a numpy array.
    :param conn: Connection object to the PostgreSQL database.
    """
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO img (filename, img_vct)
            VALUES (%s, %s::vector)
            """,
            # (image_name, vector.tolist())  # Convert numpy array to list for insertion
            (image_name, vector.tolist())  # Convert numpy array to list for insertion
        )
        conn.commit()

print ( f_prfx(), '---- functions defined ---- ' )

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname   ='postgres',
    user     ='postgres',
    password ='postgres',
    host     ='localhost',
    port     ='5432'
)

print ( f_prfx(), '---- db connetion made ---- ' )

# Example usage
img_path = 'img1.jpg'
image_name = 'first image img1'
vector = extract_vector(img_path)
store_vector_in_db(image_name, vector, conn)

# now loop over a directory
image_directory = '/Users/pdvbv/zz_imgs/'
# image_directory = '/Users/pdvbv/fotos/camera/2024_04_16/'

print ( f_prfx() ) 
print ( f_prfx(), " ---- looping over jpg files ---- " ) 

# Loop over all .jpg files in the directory
for filename in os.listdir(image_directory):
  if filename.endswith('.jpg'):
    img_path = os.path.join(image_directory, filename)
    print ( f_prfx(), "file : ", filename )
    vector = extract_vector(img_path)
    print ( f_prfx(), "file : ", filename, " extracted..."  )
    store_vector_in_db(filename, vector, conn)
    print(f"Processed and stored vector for: {filename}")
  # end if jpg
# end for loop

# show last image ?

# Close the connection
conn.close()

print ( f_prfx(), " --- done ---- " ) 
