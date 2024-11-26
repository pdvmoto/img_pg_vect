
# test_utils.py:
# - inspect_object.py  : try looking inside objects
# - duration.py        : timer utilitiy
# - prefix.py          : debug and log printing utility

import time
from datetime import datetime 

# in case we fogert..
def f_prfx():
  return " localprfx: " 

# local utilities, keep/cp in same directory for now...
from  duration      import *
from  inspect_obj   import *
from  prefix        import *

def pq ( *argv ):
  print ( f_prfx(), ' : ',  *argv )
  return 0   # consider returning nr-args, or length of string


# test code
print ( ' i-- start  : ', tmr_start() )
print ( ' i-- set    : ', tmr_set() )

time.sleep ( 1 ) 
print ( ' \n i-- dur    : ', tmr_durat() )
print ( ' i-- total  : ', tmr_total() )
print ( ' i-- dur2   : ', tmr_durat() )
print ( ' i-- re-set : ', tmr_set() )
print ( ' i-- dur4   : ', tmr_durat() )

time.sleep ( 1 ) 
print ( '\n i-- total4 : ', tmr_total() )
print (   ' i-- dur    : ', tmr_durat() )
time.sleep ( 1) 
print ( '\n i-- re-set : ', tmr_set() )
print (   ' i-- dur0   : ', f" = {tmr_durat():9.5f}" )
print (   ' i-- total5 : ', f" = {tmr_total():9.5f}" )

lst  = [1, 2,3 ]  
f_inspect_obj ( 'list ', lst ) 

print ( 'testing prefix:' , f_prfx() )
print ( f_prfx(), '..with prefix...' )

pp    ( f_prfx(), '..from pp ...' )

pp ( 'testing pp with prefix' , 1, 2, 3 )