#  rt1.py : measure round trips

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

cur_logon = ora_conn.cursor ()
for row in cur_logon.execute ( sql_test ):
  pp   ( ' ora_result : ', row )

pp    ()
pp    ( ' ----- ora_logon: tested ---- ' )
pp    ()


def f_do_roundtrips_sec ( n_secs ):
  #
  # loop for n_secs, and report the counter of nr loops done.
  #

  # return 1 row, 1 value, easiest cursor to read...
  sql1_cnt = """ select count (*) as cnt from rt1 where payload like :b_payl """
  
  # some randome like-clause
  s_payl = '%' + ''.join(random.choices(string.ascii_uppercase, k=3)) + '%'

  cur1 = ora_conn.cursor()
  cur1.execute ( sql1_cnt, b_payl=s_payl )
  rows = cur1.fetchall ()

  # for row in rows:
  #   pp (' cur1 fetched like: ', s_payl, ' row:  ', row, row[0] )

  # fetch just row-0?
  pp (' cur1 fetched like: ',   s_payl, ' row-0:', rows[0], rows[0][0] )

  n_start = time.perf_counter()
  time.sleep(0.4)
  n_end = time.perf_counter() 

  n_ela = n_end - n_start
  pp (' ' )
  pp ( 'do_rt: ', n_start, n_end, n_ela ) 
  pp (' ' )

  n_count = 0 
  n_total = 0 
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 1
    # n_total += random.randint ( 0, 1000 ) 

    s_payl = '%' + ''.join(random.choices(string.ascii_uppercase, k=3)) + '%'
    cur1.execute ( sql1_cnt, b_payl=s_payl )
    rows = cur1.fetchall ()

    # pp (' cur1 fetched like: ',   s_payl, ' row-0:', rows[0], rows[0][0] )
    n_total += rows[0][0] 

  pp (' ' )
  pp ( 'do_rt, nr loops: ', n_count, ' nr_sec: ', n_secs, ' loops/sec: ', n_count/n_secs, ' sumtot: ', n_total ) 
  pp ( 'do_rt: ms per loop: ', 1000.0 * n_secs/n_count )
  pp (' ' )

  return  n_ela #  -- -- -- roundtrips...

pp    ()
pp    ( ' ----- functions defined ----- ' )
pp    ()


# for 1 min..
f_do_roundtrips_sec ( 120.5 )

pp ( ' ----- roundtrips done -----' ) 

