# Testing oracle pythong . insert known vectors to verify cos-dist .
#
# note: refer to create-tables and query-files.. dem03_ora.sql
#

# the python code...

import os
import time as tim
from datetime import datetime, date, time, timezone

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

import array
import numpy 

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
# model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# print ( f_prfx(), '---- model loaded ---- ' )

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

  # do the insert, input-bind-var => local_var
  img_cur.execute ( sql, fname=img_path, binary_image=binary_image, img_id=img_id ) 

  # catch out-var
  retval = img_id.getvalue()[0]

  print ( f_prfx(), ' ---- stored, retval was: ', retval, ' ---- ' ) 

  # return
  return retval

# -------- end store_imge_ora ------- 

# -------- need input type handler.. ? ---- 

# determine type..
def numpy_converter_in(value):
    if value.dtype == numpy.float64:
        dtype = "d"
    elif value.dtype == numpy.float32:
        dtype = "f"
    elif value.dtype == numpy.uint8:
        dtype = "B"
    else:
        dtype = "b"
    return array.array(dtype, value)

# return corsur-var for inserting vector
def input_type_handler(cursor, value, arraysize):
    if isinstance(value, numpy.ndarray):
        return cursor.var(
            oracledb.DB_TYPE_VECTOR,
            arraysize=arraysize,
            inconverter=numpy_converter_in,
        )

# get vector from image return numpy.ndarry ?  
def extract_vector(img_path):
    """
    Extract feature vector from an image using ResNet50.
    
    :param img_path: Path to the image file.
    :return: Feature vector as a numpy array.
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = numpy.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array)
    np_arr = features.flatten()

    print ( f_prfx(), " -- np_arr: ", np_arr )

    print ( f_prfx(), " -- np_arr.ndim  ", np_arr.ndim ) 
    print ( f_prfx(), " -- np_arr.shape ", np_arr.shape ) 
    print ( f_prfx(), " -- np_arr.size ", np_arr.size ) 
    print ( f_prfx(), " -- np_arr.dtype ", np_arr.dtype ) 
    print ( f_prfx(), " -- np_arr.itemsize ", np_arr.itemsize ) 

    # vect =  array.array(dtype, np_arr)
    # print ( f_prfx(), " ---- vect: ", vect )

    return np_arr

def store_vector_in_ora(filename, img_id, img_vector, conn):

  sql =  """
  insert into vec_img_vect ( img_id,      img_vector,  gen_by  )
                    values ( :stored_id,  :vector,     'by p3' )
  returning id into :vect_id
  """

  # cursor
  vec_cur = ora_conn.cursor()

  # variable to catch out
  vect_id = vec_cur.var(int)

  # do the insert, input-var => bind-var
  vec_cur.execute ( sql, stored_id=img_id, vector=img_vector, vect_id=vect_id ) 

  # catch the out-var and return it, in case we need it later
  retval = vect_id.getvalue()[0]

  print ( f_prfx(), ' ---- stored, vect_id was: ', retval, ' ---- ' ) 

  return retval

  # ---- end of store_vector_in_db oracle  ------- 

def store_vector_in_tv(filename, img_vector, conn):

  sql =  """
  insert into tv (  img_vector,  fname  )
          values (  :vector,     :fname )
  returning id into :vect_id
  """

  # cursor
  vec_cur = ora_conn.cursor()

  # variable to catch out
  vect_id = vec_cur.var(int)

  # do the insert, input-var => bind-var
  vec_cur.execute ( sql, vector=img_vector, fname=filename, vect_id=vect_id ) 

  # catch the out-var and return it, in case we need it later
  retval = vect_id.getvalue()[0]

  print ( f_prfx(), ' ---- stored, vect_id was: ', retval, ' ---- ' ) 

  return retval


print ( f_prfx(), '---- functions defined ---- ' )

# Connect to the oracle database, and print version

ora_conn = oracledb.connect(user="scott", password="tiger",
                              host="localhost", port=1521, service_name="freepdb1")

cursor = ora_conn.cursor()
for row in cursor.execute("select * from v$version"):
    print( f_prfx(), row )

# define the input type handler, this will convert numpy arrays to vectors ?
ora_conn.inputtypehandler = input_type_handler

print ( f_prfx(), '---- db connetion made, handler defined ---- ' )

# -- Example usage
# img_path = 'img1.jpg'
# image_name = 'first image img1'
# stored_id = store_image_ora ( img_path , ora_conn ) 
# print ( f_prfx(), ' ---- img stored, id ', stored_id, ' ---- ' ) 

# -- generate vector and store in db
# vector = extract_vector(img_path)
# store_vector_in_db(image_name, vector, ora_conn)

# generate arrays with all zeros and all 1s

nparr_0s = numpy.zeros ( 2048, float )
nparr_1s = numpy.ones  ( 2048, float )
nparr_2s = numpy.full  ( 2048, 2.0, float )

# stored_id = store_vector_in_tv("zeros", nparr_0s, ora_conn)
stored_id = store_vector_in_tv("ones" , nparr_1s, ora_conn)
# stored_id = store_vector_in_tv("twos" , nparr_2s, ora_conn)

# now set 1 value and add..
nparr_1s[0] = 2.0
stored_id = store_vector_in_tv("one2" , nparr_1s, ora_conn)

ora_conn.commit () 

# -- now loop over a directory
image_directory = '/Users/pdvbv/tmp/'
# image_directory = '/Users/pdvbv/zz_imgs/'
# image_directory = '/Users/pdvbv/fotos/camera/2024_04_16/'
# image_directory = '/Users/pdvbv/Fotos/camera/2023_10_10'

print ( f_prfx() ) 
print ( f_prfx(), " ---- looping over jpg files ---- " ) 

# -- Loop over all .jpg files in the directory
for filename in os.listdir(image_directory):
  if filename.endswith('.jpg'):

    img_path = os.path.join(image_directory, filename)
    print ( f_prfx(), "file : ", filename )

    stored_id = store_image_ora ( img_path , ora_conn ) 
    print ( f_prfx(), ' ---- loops-file stored, id ', stored_id, ' ---- ' ) 

    vector = extract_vector(img_path)
    print ( f_prfx(), "file : ", filename, " extracted..."  )

    store_vector_in_ora(filename, stored_id, vector, ora_conn)

    print(f_prfx(), f"Processed and stored vector for: {filename}", ", id= ", stored_id )

    ora_conn.commit()

  # end if jpg
# end for loop

# show last image ?

# Close the connection
ora_conn.commit () 
ora_conn.close()

print ( f_prfx(), " --- done ---- " ) 
