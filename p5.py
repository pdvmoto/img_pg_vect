# Testing oracle pythong . "how to store images and vectors in database"
#
# note: refer to create-tables and query-files.. ct_vecimg.sql
#

# the python code...

import os
import time as tim
from datetime import datetime, date, time, timezone

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image

import numpy 
import array

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

def store_image_ora ( img_dir, img_fn , ora_conn ):
  """
  store the blob and return the id in table vec_img
  """

  # needs 4 arguments: dir, fn, data and out-id
  sql =  """
  INSERT INTO vec_img  ( fpath,  fname,  img_data,      remarks)
              VALUES  ( :fpath, :fname,  :binary_image, 'some remark' )
  RETURNING id INTO :img_id
  """
  
  # pick up the image from file
  with open( img_dir + img_fn, "rb") as image_file:
    binary_image = image_file.read()

  # cursor and variable to catch Returning..
  img_cur = ora_conn.cursor()
  img_id  = img_cur.var(int)

  # do the insert, input-bind-var => local_var
  img_cur.execute ( sql, fpath=img_dir, fname=img_fn, binary_image=binary_image, img_id=img_id ) 

  # catch out-var
  retval = img_id.getvalue()[0]

  print ( f_prfx(), ' ---- stored, retval img_id: ', retval, ' ---- ' ) 

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

    # print ( f_prfx(), " -- np_arr.ndim  "   , np_arr.ndim ) 
    # print ( f_prfx(), " -- np_arr.shape "   , np_arr.shape ) 
    # print ( f_prfx(), " -- np_arr.size "    , np_arr.size ) 
    print ( f_prfx(), " -- np_arr.dtype "   , np_arr.dtype ) 
    # print ( f_prfx(), " -- np_arr.itemsize ", np_arr.itemsize ) 

    return np_arr  
    # -------------- end: extract_vector ------ 

 
def store_vector_in_ora(img_id, img_vector, conn):

  sql =  """
  insert into vec_img_vect ( img_id,      img_vector,  gen_by  )
                    values ( :stored_id,  :bind_vect,  'stored by p3.py' )
  returning id into :vect_id
  """

  sql =  """
  insert into vec_img_vect ( img_id,        gen_by  )
                    values ( :stored_id,    'stored by p3.py' )
  returning id into :vect_id
  """

  # cursor
  vec_cur = ora_conn.cursor()

  # variable to catch returning 
  vect_id = vec_cur.var(int)
  
  # using array, and remove need for iput handler?
  # note: hardcoded type d is a float-64, but column is f=float32 ? 
  new_arr = array.array ( "d", img_vector )   # but vector is numpy-array float32 ??
  # new_arr =  img_vector.tolist()  # try with list
  # new_arr = img_vector 

  # print ( f_prfx(), " -- new_arr: ", new_arr )

  # print ( f_prfx(), " -- new_arr.ndim  "   , len (new_arr ) ) 
  # print ( f_prfx(), " -- new_arr.shape "   , new_arr.shape ) 
  # print ( f_prfx(), " -- new_arr.size "    , new_arr.size ) 
  # print ( f_prfx(), " -- new_arr.dtype "   , new_arr.dtype ) 
  # print ( f_prfx(), " -- new_arr.itemsize ", new_arr.itemsize ) 

  # do the insert, :bind_var => local-var 
  # vec_cur.execute ( sql, stored_id=img_id, bind_vect=img_vector, vect_id=vect_id ) 
  # vec_cur.execute ( sql, stored_id=img_id, bind_vect=new_arr, vect_id=vect_id ) 

  # try creating + update
  vec_cur.execute ( sql, stored_id=img_id, vect_id=vect_id ) 

  # catch the out-var and return it, in case we need it later
  retval = vect_id.getvalue()[0]

  print ( f_prfx(), ' -- created vect_id: ', retval, ' ---- ' ) 
 
  # now fresh cursor to update
  cur2 = ora_conn.cursor()
  # cur2.execute ( "update vec_img_vect set img_vector = :1 where img_id = :2 " , [ new_arr, img_id ]  )
  cur2.execute ( "update vec_img_vect set img_vector = :1 where id = :2 " , [ new_arr, retval ]  )

  # put vectordata in file again..
  # dbgdata = 'stored_' + str(img_id) + '.out'
  # n_elem = vector_to_file ( img_vector, dbgdata )

  return retval

  # ---- end of store_vector_in_db postgres ------- 


def vector_to_file ( vec, fname ):
  """ store vector values to file for debug...
  """

  outfil = open ( fname, 'a' )

  for indx in range ( 0, len( vec) ):
    # print ( f_prfx(), ' elem : ', indx, ' value: ', vec[indx] )
    outfil.write ( ' elem: ' + str (indx) +  ' value: ' + str ( vec[indx] ) + '\n' ) 

  outfil.close()

  return indx
  # -- vector_to_file ---- ---------
 
print ( f_prfx(), '---- functions defined ---- ' )

# Connect to the oracle database, and print version

ora_conn = oracledb.connect(user="scott", password="tiger",
                              host="localhost", port=1521, service_name="freepdb1")

# input type handler, this will convert numpy arrays to vectors ?
# ora_conn.inputtypehandler = input_type_handler

cursor = ora_conn.cursor()
for row in cursor.execute("select * from v$version"):
    print( f_prfx(), row )

print ( f_prfx(), '---- db connetion made ---- ' )

# -- now loop over a directory
image_directory = '/Users/pdvbv/zz_imgs/'
# image_directory = '/Users/pdvbv/fotos/camera/2024_04_16/'
# image_directory = '/Users/pdvbv/Fotos/camera/2023_10_10/'

print ( f_prfx() ) 
print ( f_prfx(), " ---- looping over jpg files ---- " ) 

# to debug cos-dist.. initiate a prev_vect, 
# and compare every 2 vectors 
prev_vect =  numpy.ones ( 2048, numpy.float32 ) 
vect      =  numpy.ones ( 2048, numpy.float32 ) 

# -- Loop over all .jpg files in the directory
for filename in os.listdir(image_directory):
  if filename.endswith('.jpg'):

    img_path = os.path.join(image_directory, filename)
    print ( f_prfx(), " ---- file : ", filename, ' ---- '  )

    vec_img_id  = store_image_ora ( image_directory, filename, ora_conn ) 
    # print ( f_prfx(), ' ---- img_id ', vec_img_id ' ---- ' ) 

    vect = extract_vector(img_path)

    # print ( f_prfx(), " ---- file : ", filename, " extracted..."  )

    # dbgdata = 'dbg_' + str(vec_img_id) + '.out'
    # n_elem = vector_to_file ( vect, dbgdata )
    # print ( f_prfx(), '-- saved, array len: ', n_elem, ' to file: ', fdata )

    vec_img_vect_id = store_vector_in_ora(vec_img_id, vect, ora_conn)

    print(f_prfx(), f" ---- Processed and stored vector for: {filename}", ", img_id= ", vec_img_id, " vect_id:", vec_img_vect_id )

    ora_conn.commit()

    # verify: cos distan with prev.
    cos_dist =  numpy.dot(prev_vect, vect) / (numpy.linalg.norm(prev_vect) * numpy.linalg.norm(vect)) 
    print ( f_prfx(), ' -- Cos similiary with previous: ', cos_dist, ' ---- ' )

    # keep vector to calculate cos-dist with next
    prev_vect = vect

  # end if jpg
# end for loop

# show last image ?

# Close the connection
ora_conn.commit () 
ora_conn.close()

print ( f_prfx(), " --- done ---- " ) 
