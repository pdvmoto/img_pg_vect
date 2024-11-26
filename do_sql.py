#
# do_sql.py : enter a query and run it, print results
#
# background:
#   just bcse I need to learn, and I think may be useful
#   also: I needded a test-template to test utilities..
#
# Stern Warning: 
#   This tool uses "dynamic SQL", 
#   and is Thus susceptible to SQL-Injections.
#   (hey, this tool IS exactly that: SQL-Injection,
#    Deal With It. ;-)
#
# todo:
# - consider using conn_name from SQLcl
# - also output to file e.g. a.out ( but pipe-tee a.out works fine)
# - allow for a pager, and space / enter / nr to continue (never if arg-1 provided)
# - allow silent or scripted run: dont require keyboard input (+/- done)
# - devise some automated testing, and test more extensively
# - Graceful Exit on SQL-error (gently report ORA-00942 etc..).
# - enable use with other drivers, databases as well
# - remove need for quotes around arg[1] (nah...)
# - provide for -h --h, --help..
# - lots more, but not prio atm
#

print ( ' ' ) 
print ( '--------- do_sql.py: enter manual queries... ---------- ' )
print ( ' ' ) 

import    os
import    sys
import    array

import    time
from      datetime      import datetime
from      dotenv        import load_dotenv

import    oracledb 

print ( ' ' )
print ( "--------- generic imports done  -------------- " )
print ( ' ' )

from      duration      import *
from      inspect_obj   import *
from      prefix        import *


pp    ( ' ' )
pp    ( "--------- local utilities imports done  -------------- " )
pp    ( ' ' )



sql_show_conn="""
  select 2 as ordr
     , 'version : ' ||  substr ( banner_full, -12) as txt
  from v$version 
UNION ALL
  select 1
     , 'user    : '|| user || ' @ ' || global_name|| ' ' as txt
  FROM global_name     gn
UNION ALL
  SELECT 3        
     , 'prompt  : ' || user
       || ' @ ' ||db.name
       || ' @ '|| SYS_CONTEXT('USERENV','SERVER_HOST')
       || decode  (SYS_CONTEXT('USERENV','SERVER_HOST')
            , 'ip-172-20-2-109', ' (PROD)'
            , 'ip-172-20-0-226', ' (ACC)'
            , 'ip-172-20-0-23',  ' (SE)'
            , '98b6d46dd637',    ' (xe-dev)'
            , '98eac28a59c0',    ' (dckr-23c)'
            , '2c4a51017a44',    ' (dckr-23ai)'
            , ' (-envname-)')
       || ' > '
  FROM    v$database      db
order by 1
"""

err_no_list="""
..
.. Warning: 
..
.. Query result is not a vector/list.
.. Please provide a Query that returns a List (vector) as first column.
..
.. Example: Select vector from table ;
..
"""

pp    ( ' ' ) 
pp    ( '--------- constants defined ... ---------- ' )
pp    ( ' ' ) 


# ---- chop off semicolon ---- 

def chop_off_semicolon ( qrystring ):

  retval = str.rstrip ( qrystring )
  n_last = len(retval) - 1

  if retval [ n_last ] == ';':
    retval = retval[:-1] 
    # print( 'sql stmnt chopped: [', retval, ']' )

  return retval # ---- chopped off semincolon ---- 


# --- the output handle: need this to convert vector to list ------ 

def output_type_handler(cursor, metadata):
    if metadata.type_code is oracledb.DB_TYPE_VECTOR:
        return cursor.var(metadata.type_code, arraysize=cursor.arraysize,
                          outconverter=list)

# ------ start of main ---------- 


pp    ( ' ' ) 
pp    ( '--------- functions defined, start of main..  ---------- ' )
pp    ( ' ' ) 

  
# get env, which should contain the connecion variables, no dflts provided..
 
load_dotenv()
  
# get + verify..   
ora_user    = os.getenv ( 'ORA_USER' )
ora_pwd     = os.getenv ( 'ORA_PWD' )
ora_server  = os.getenv ( 'ORA_SERVER' )
ora_port    = os.getenv ( 'ORA_PORT' )
ora_sid     = os.getenv ( 'ORA_SID' )

# verify... dont print this at work.
pp    ( f_prfx() + ora_user + ' / ****** @ ' + ora_server , ' ; ' + ora_port + ' \\ ' + ora_sid )
  
  
ora_conn = oracledb.connect (
    user          = ora_user
  , password      = ora_pwd    
  , host          = ora_server 
  , port          = ora_port   
  , service_name  = ora_sid    
)

print ( f_prfx(), ' --- Connection is: --->' )

cursor = ora_conn.cursor()
for row in cursor.execute ( sql_show_conn ):
  pp   ( row )

print( f_prfx(), '<-- Connection ' )

pp    ( ' ' )
pp    ( "-----------------  connection opened ------------- " )
pp    ( ' ' )

# quit ()

# prepare to handle vectors -> lists 
# sigh, do I really have to specify this... ?
ora_conn.outputtypehandler = output_type_handler


# --- check arguments ----- 

n = len(sys.argv)

# Arguments passed
# print("Name of Python script:", sys.argv[0])
# print("Total arguments passed:", n)
# print("Arguments passed:")
# for i in range(1, n):
#   print('..arg ' , i, ': [', sys.argv[i], ']')

# now start sql and real work

# sql_for_vector=""" select vect from img_vector  where id = 1 """
# sql_for_vector=""" select img_vector from vec_img_vect where id = 1 """

# if arg1: use it as SQL..
if len(sys.argv) == 2:
  sql_for_qry = sys.argv[1] 
else:
  print ( ' ' )
  sql_for_qry = input ( "do_py: SQL > " )

sql_for_qry = chop_off_semicolon ( sql_for_qry ) 

pp    ( ' ' )
pp    ( ' processing...' )
pp    ( ' ' )

rowcnt = 0
cursor = ora_conn.cursor()
for row in cursor.execute ( sql_for_qry ):
  rowcnt = rowcnt + 1 
  pp   ( row )

pp    ( ' ' )
pp    ( rowcnt, ' rows processed.' ) 
pp    ( ' ' )


pp    ( ' ' ) 
pp    ( '.. Query was          : [', sql_for_qry, ']' )
pp    ( ' ' ) 

