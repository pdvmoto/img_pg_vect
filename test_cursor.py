
# test_utils.py:
# - inspect_object.py  : try looking inside objects
# - duration.py        : timer utilitiy
# - prefix.py          : debug and log printing utility
# - ora_logon.py

print ( ' ---- test_cursor.py --- ' ) 

print ( ' ---- test_cursor.py first do imports ..--- ' ) 

import    time
from      datetime  import  datetime 

print ( 'for the record: perfcount and process_time: ', time.perf_counter(), time.process_time() )
print ()

# in case we forget..
def f_prfx():
  return " localprfx: " 

# local utilities, keep/cp in same directory for now...
from  duration      import *
from  inspect_obj   import *
from  prefix        import *
from  ora_login     import *


# test code
pp    ()
pp    ( ' ----- imports done, now testing duration.py ---- ' ) 
pp    ()

print ( ' -- start  : ', tmr_start() )
print ( ' -- set    : ', tmr_set() )

time.sleep ( 1 ) 
print ( ' \n -- dur    : ', tmr_durat() )
print ( ' -- total  : ', tmr_total() )
print ( ' -- dur2   : ', tmr_durat() )
print ( ' -- re-set : ', tmr_set() )
print ( ' -- dur4   : ', tmr_durat() )

time.sleep ( 1 ) 
print ( '\n -- total4 : ', tmr_total() )
print (   ' -- dur    : ', tmr_durat() )
time.sleep ( 1) 
print ( '\n -- re-set : ', tmr_set() )
print (   ' -- dur0   : ', f" = {tmr_durat():9.5f}" )
print (   ' -- total5 : ', f" = {tmr_total():9.5f}" )

pp    ()
pp    ( ' ----- testing inspect_obj.py ---- ' ) 
pp    ()

lst  = [1, 2,3 ]  
f_inspect_obj ( 'list ', lst ) 

pp    ()
pp    ( ' ----- next testing prefix..  ---- ' ) 
pp    ()
pp    ( f_prfx(), '..with double? prefix...' )

pp    ( 'prefix = [' + f_prfx() + '] ..from pp ...' )

pp    ( 'testing pp with prefix' , 1, 2, 3 )

pp    ()
pp    ( ' ---- prefix done, next test ora_login ---- ' ) 
pp    ()


# call the imported logon..
ora_conn = ora_logon ()

sql_test = """
  select object_type, count (*) 
    from user_objects
   group by object_type   
"""

cur_logon = ora_conn.cursor ()
for row in cur_logon.execute ( sql_test ):
  pp   ( ' ora_result : ', row )
    
pp    () 
pp    ( ' ----- ora_logon: tested ---- ' )
pp    ()

pp    ()
pp    ( ' ----- testing inspect_obj.py: ora_con ---- ' ) 
pp    ()

f_inspect_obj ( 'ora_conn ', ora_conn )

pp    ()
pp    ( ' ----- testing inspect_obj.py: oraa_cursor ---- ' ) 
pp    ()

f_inspect_obj ( 'cur_logon ', cur_logon )

pp ()
pp ( ' ----- cursor: arraysize: ', cur_logon.arraysize )
pp ( ' ----- cursor: statement: ', cur_logon.statement ) 
pp ()

pp ( ' ----- testing done..  ---- ' ) 
