# Testing oracle pythong . "how to store images and vectors in database"
#
# note: refer to create-tables and query-files.. ct_vecimg.sql
#


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

# import psycopg2
import oracledb


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

print ( f_prfx(), '---- model loaded ---- ' )

def store_image_ora ( img_path , ora_conn ):
  """
  create vec_img record, just store the blob and return the id
  """

  # needs three arguments: fn, data and out-id
  sql =  """
  INSERT INTO vec_img (fname,  img_data,      remarks)
              VALUES (:fname,  :binary_image, 'some remark' )
  RETURNING id INTO :img_id
  """
  
  # pick up the image from file
  with open(img_path, "rb") as image_file:
    binary_image = image_file.read()

  # cursor
  img_cur = ora_conn.cursor()

  # variable to catch out
  img_id = img_cur.var(int)

  # do the insert, input-var => bind-var
  img_cur.execute ( sql, fname=img_path, binary_image=binary_image, img_id=img_id ) 

  # catch out-var
  retval =img_id.getvalue() 

  print ( f_prfx(), ' ---- stored, reval was: ', retval, ' ---- ' ) 

  # return
  return retval

# -------- end store_imge_ora ------- 

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

# Connect to the oracle database, and print version

ora_conn = oracledb.connect(user="scott", password="tiger",
                              host="localhost", port=1521, service_name="freepdb1")

cursor = ora_conn.cursor()
for row in cursor.execute("select * from v$version"):
    print( f_prfx(), row )

print ( f_prfx(), '---- db connetion made ---- ' )

# Example usage
img_path = 'img1.jpg'
image_name = 'first image img1'
store_image_ora ( img_path , ora_conn ) 

ora_conn.commit () 


# generate vector and store in db
vector = extract_vector(img_path)
# store_vector_in_db(image_name, vector, ora_conn)

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

    store_image_ora ( img_path , ora_conn ) 

    vector = extract_vector(img_path)
    print ( f_prfx(), "file : ", filename, " extracted..."  )
    # store_vector_in_db(filename, vector, conn)
    print(f"Processed and stored vector for: {filename}")

  # end if jpg
# end for loop

# show last image ?

# Close the connection
ora_conn.commit () 
ora_conn.close()

print ( f_prfx(), " --- done ---- " ) 
