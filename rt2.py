#  rt2.py : spool out table and report round-trips
#  
# note: make sure records is "too big" for 1 roundtrip ? 

print ( ' ---- rt1.py --- ' )

print ( ' ---- rt1.py first do imports ..--- ' )

import    time
import    string
from      datetime  import  datetime
import    random

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


ora_conn = ora_logon ()

sql_test = """
  select object_type, count (*)
    from user_objects
   group by object_type
"""

# cur_logon = ora_conn.cursor ()
# for row in cur_logon.execute ( sql_test ):
#   pp   ( ' ora_result : ', row )

pp    ()
pp    ( ' ----- ora_logon: done ---- ' )
pp    ()


def f_do_roundtrips_spool ( n_secs ):
  #
  # loop for n_secs, and report the counter of nr loops done.
  #

  # return 1 row, 1 value, easiest cursor to read...
  sql1_cnt = """ select count (*) as cnt from rt1 where payload like :b_payl """
  sql2_all = """ select * from rt1 """

  sql3_stats = """ select name, value 
    from v$mystat m, v$statname n
    where n.statistic# = m.statistic#
    and ( name like '%roundtrips to/from client%'
        or name like '%equests to%'
      ) """
  
  cur1 = ora_conn.cursor()
  rowcnt = 0
  for row in cur1.execute ( sql2_all ):
    rowcnt += 1 
    pp   ( row )      

  pp (' ' )
  pp ( 'do_rt, nr loops: ', rowcnt ) 
  # pp ( 'do_rt: ms per loop: ', 1000.0 * n_secs/n_count )
  pp (' ' )

  pp (' ' )
  pp (' ---- Stats: ---- ' )
  pp (' ' )

  rowcnt = 0
  for row in cur1.execute ( sql3_stats ):
    rowcnt += 1 
    pp   ( row )      

  pp (' ' )
  pp ( 'do_rt, nr loops: ', rowcnt ) 
  # pp ( 'do_rt: ms per loop: ', 1000.0 * n_secs/n_count )
  pp (' ' )

  return  rowcnt #  -- -- -- roundtrips...

pp    ()
pp    ( ' ----- functions defined ----- ' )
pp    ()


# for 1 min..
f_do_roundtrips_spool ( 120.5 )

pp ( ' ----- roundtrips done -----' ) 

