#  rt3_ping.py : loop + time heath + ping of coonnection
#  
# note: make sure records is "too big" for 1 roundtrip ? 

print ( ' ---- rt3.py --- ' )

print ( ' ---- rt3.py first do imports ..--- ' )

import    time
import    string
from      datetime  import  datetime
# import    random

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
ora_con2 = ora_logon ()

sql_test = """
  select object_type, count (*)
    from user_objects
   group by object_type
"""

cur_logon = ora_conn.cursor ()
for row in cur_logon.execute ( sql_test ):
  pp   ( ' ora_result : ', row )

pp    ()
pp    ( ' ----- ora_logon: done ---- ' )
pp    ()


def f_do_pings ( n_secs ):
  #
  # loop for n_secs, and report the counter of nr loops done.
  #

  n_count = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 1
    # empty loop 

  ms_p_loop = 1000.0 * n_secs/n_count 

  pp (' ' )
  pp ( 'nr empty loops: ', n_count, ' loops/sec: ', n_count/n_secs )
  pp ( 'ms per loop: ', ms_p_loop )
  pp (' ' )

  n_count = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 2
    ora_conn.is_healthy()
    ora_con2.is_healthy()

  ms_p_health = 1000.0 * n_secs/n_count 

  pp (' ' )
  pp ( 'nr empty heaalth: ', n_count, ' loops/sec: ', n_count/n_secs )
  pp ( 'ms per heaalth: ', ms_p_health )
  pp (' ' )

  n_count = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 2
    ora_conn.ping()
    ora_con2.ping()

  ms_p_ping = 1000.0 * n_secs/n_count 

  pp (' ' )
  pp ( 'nr empty ping: ', n_count, ' loops/sec: ', n_count/n_secs )
  pp ( 'ms per ping: ', ms_p_ping )
  pp (' ' )

  return  n_secs #  -- -- -- roundtrips...


pp    ()
pp    ( ' ----- functions defined ----- ' )
pp    ()


# for 1 min..
f_do_pings ( 15.0 )

pp ( ' ----- roundtrips done -----' ) 

