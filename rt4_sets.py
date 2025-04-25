#  rt3_ping.py : loop + time heath + ping of coonnection
#  
# note: make sure records is "too big" for 1 roundtrip ? 

print ( ' ---- rt3.py --- ' )

print ( ' ---- rt3.py first do imports ..--- ' )

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
pp    ( ' ----- imports done, now testing ---- ' )
pp    ()

print ( ' -- start  : ', tmr_start() )
print ( ' -- set    : ', tmr_set() )

def f_chatty_info ():
  # 
  # output network and other stats from session 
  # 
  sql_stats = """
    select sn.name, st.value
    --, st.* 
    from v$mystat st
    , v$statname sn
    where st.statistic# = sn.statistic# 
    and ( sn.name like '%roundtrips%'
        or sn.name like 'bytes sent%'
        or sn.name like 'bytes rec%'
        or sn.name like '%execute count%'
        or sn.name like 'user calls'
        or sn.name like 'user commits'
        or sn.name like 'user rollbacks'
        or sn.name like 'consistent gets'
        or sn.name like 'db block gets'
        or sn.name like 'opened cursors current'
        )
      order by sn.name 
  """

  pp ( ' Report out Session Stats ' ) 

  cur_stats = ora_conn.cursor()
  for row in cur_stats.execute ( sql_stats ):
    # pp   ( ' stats : ', row[1], ' ', row[0] )
    pp   ( ' ', f"{row[1]:10d}  {row[0]}"   )

  return 0 # -- -- -- -- f_chatty_info


sql_test = """
  select object_type, count (*)
    from user_objects
   group by object_type
"""

def f_do_pings ( n_secs ):
  #
  # loop for n_secs, and report the counter of nr loops done.
  #

  n_count = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 1
    # empty loop 

  n_dur = time.perf_counter() - n_start
  ms_p_loop  = 1000.0 * n_secs /n_count 
  ms_p_loop2 = 1000.0 * n_dur  /n_count 

  pp (' ' )
  pp ( 'n_sec and actual dur  : ', n_secs, ' ', n_dur )
  pp ( 'nr empty loops        : ', n_count, ' loops/sec: ', n_count/n_secs, ' better: ', n_count/n_dur )
  pp ( 'ms per loop  and _2   : ', ms_p_loop, ' more exact: ', ms_p_loop2 )
  pp (' ' )

  # n_count = 0
  # n_start = time.perf_counter()
  # while time.perf_counter() - n_start < n_secs:
  #   n_count += 1
  #   ora_conn.is_healthy()

  # ms_p_health = 1000.0 * n_secs/n_count 

  # pp (' ' )
  # pp ( 'nr empty heaalth: ', n_count, ' loops/sec: ', n_count/n_secs )
  # pp ( 'ms per heaalth  : ', ms_p_health )
  # pp (' ' )

  n_count = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 1
    ora_conn.ping()
    # ora_con2.ping()

  n_dur = time.perf_counter() - n_start
  ms_p_loop  = 1000.0 * n_secs /n_count 
  ms_p_loop2 = 1000.0 * n_dur  /n_count 

  pp (' ' )
  pp ( 'n_sec and actual dur  : ', n_secs, ' ', n_dur )
  pp ( 'nr empty ping         : ', n_count, ' loops/sec: ', n_count/n_secs, ' better: ', n_count/n_dur )
  pp ( 'ms per ping  and _2   : ', ms_p_loop, ' more exact: ', ms_p_loop2 )
  pp (' ' )

  return  n_secs #  -- -- -- roundtrips...

def f_do_sql ( n_secs ):
  # 
  #  do SQL-fetches, and report time and ms per loop
  # 
  sql_dual = """ 
    select to_number ( to_char ( sysdate, 'SS' ) ) from dual
  """
  # or..return 1 row, 1 value, easiest cursor to read...
  sql1_cnt = """ select id id, substr ( payload, 1, 5) as payload 
      from rt1 
      where payload like :b_payl 
      order by 2 desc """

  # sql1_cnt = """ select count (*) as cnt from dual """

  cur_cnt = ora_conn.cursor()
  cur_cnt.arraysize = 1

  n_count = 0
  n_rows  = 0
  n_total = 0
  n_start = time.perf_counter()
  while time.perf_counter() - n_start < n_secs:
    n_count += 1

    # randome string of k..
    s_payl = '%' + ''.join(random.choices(string.ascii_uppercase, k=4)) + '%'
    # cur_cnt.execute ( sql1_cnt )
    cur_cnt.execute ( sql1_cnt, b_payl=s_payl )
    rows = cur_cnt.fetchall ()

    pp (' cur1 fetched like: ',   s_payl, ' nr_recs: ', len(rows) )

    for row in rows:
      n_rows += +1
      # pp (' cur1 fetched row: ', row )

  # end of while-n_secs.

  n_dur = time.perf_counter() - n_start
  ms_sql = 1000.0 * n_dur/n_count 

  pp (' ' )
  pp ( 'n_sec, n_dur    : ', n_secs, ' ', n_dur )
  pp ( 'n_count         : ', n_count )
  pp ( 'n_rows          : ', n_rows )
  pp ( 'nr fetch-alls   : ', n_count, ' loops/sec: ', n_count/n_secs )
  pp ( 'ms per fetchall : ', ms_sql )
  pp (' ' )

  return n_secs # -- -- -- f_do_sql, looped over sql


def f_do_sql_fetchone ( n_secs ):
  # 
  #  do SQL-fetches, use fetchone
  # 
  sql_dual = """ 
    select to_number ( to_char ( sysdate, 'SS' ) ) from dual
  """
  # or..return 1 row, 1 value, easiest cursor to read...
  sql1_cnt = """ select id id, substr ( payload, 1, 5) as payload 
      from rt1 
      where payload like :b_payl 
      order by 2 desc """
  # sql1_cnt = """ select count (*) as cnt from dual """

  cur_cnt = ora_conn.cursor()

  # impact! 
  # cur_cnt.arraysize = 3

  n_loopcnt = 0
  n_execnt  = 0
  n_rows    = 0
  n_total = 0
  n_start = time.perf_counter()

  while time.perf_counter() - n_start < n_secs:

    n_loopcnt += 1

    # randome string of k..
    s_payl = '%' + ''.join(random.choices(string.ascii_uppercase, k=4)) + '%'

    n_execnt = 0
    for row in cur_cnt.execute ( sql1_cnt, b_payl=s_payl ):
      n_execnt += 1 
      n_rows   += 1
      # pp (' cur1 fetched row: ', row, ', row0: ', row[0] )

    # end for cursor

    pp (' cur1 fetched like: ',   s_payl, ' nr_recs_in_cur: ', n_execnt, ' total: ', n_rows )

  # end of while n_secs.

  n_dur = time.perf_counter() - n_start
  ms_sql = 1000.0 * n_dur/n_rows 

  pp (' ' )
  pp ( 'n_sec, n_dur    : ', n_secs, ' ', n_dur )
  pp ( 'n_loopcnt       : ', n_loopcnt )
  pp ( 'n_rows          : ', n_rows )
  pp ( 'nr fetch-alls   : ', n_loopcnt, ' loops/sec: ', n_loopcnt/n_dur )
  pp ( 'ms per row : ', ms_sql )
  pp (' ' )

  return n_secs # -- -- -- f_do_sql_fetchone, looped over sql

pp    ()
pp    ( ' ----- functions defined, starting actual program ----- ' )
pp    ()


# dflt duration here...
n_secs = 10.0

if len(sys.argv) > 1:
  n_secs = float ( sys.argv[1] )

pp    ()
ora_conn = ora_logon ()
pp    ()

pp    ()
pp    ( ' ----- ora_logon: done ---- ' )
pp    ()

# for n_secs  ..
f_do_pings ( n_secs )

pp    ()
pp    ( ' ----- pings done ----- ' )
pp    ()

# show stats for this connection..
ora_sess_info ( ora_conn )

pp    ()
pp    ( ' ----- ora_logon: new connection  ---- ' )
pp    ()

ora_conn = ora_logon ()
f_do_sql ( n_secs )

pp    ()
pp    ( ' ----- sql done ----- ' )
pp    ()

# show stats for this connection..
ora_sess_info ( ora_conn )

ora_conn = ora_logon ()
f_do_sql_fetchone ( n_secs )

pp    ()
pp    ( ' ----- sql done ----- ' )
pp    ()

# show stats for this connection..
ora_sess_info ( ora_conn )

pp    ()
pp ( ' ----- roundtrips done -----' ) 

