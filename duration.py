
import time
from datetime import datetime 

# duration.py: measure duration of programs or tasks.
# 
# usage: 
#   from duration import *
#
# functions:
# - tmr_start() : set start point, return now()    global variable: g_start_total
# - tmr_total() : get sec since tmr_total, stopwatch from start of program
# - tmr_set()   : set point to measure, now(), also re-sset.. global_var: g_start_dur
# - tmr_durat() : get duration in sec/ms since last set, the stopwatch inside the program
# - tmr_spin()  : spin on full-CPU for nr of n_sec (can be float) - Spinning/running Wait...
# 
# todo: 
# - investigate time vs datetime packages, prefer only 1
# - use more than 1 timer..so they dont interfere. allow nested timeing
# - use generic trick to time total of a program-run
#

# ----- timers here ---- 

# define global vars, of type now()
g_tmr_total = datetime.now()
g_tmr_durat = datetime.now()

def tmr_start ():
  global g_tmr_total
  g_tmr_total = datetime.now()
  return g_tmr_total  # later: epoch-seconds..  

def tmr_set ():
  global g_tmr_durat
  g_tmr_durat = datetime.now()
  return g_tmr_durat  # later: epoch-seconds?

def tmr_total ():
  elapsed = ( datetime.now() - g_tmr_total ).total_seconds()
  return  elapsed

def tmr_durat ():
  durat = ( datetime.now() - g_tmr_durat ).total_seconds()
  return  durat

def tmr_spin ( spin_s: float ):

  start_t = datetime.now().timestamp()        # time.time()
  end_t   = start_t + spin_s 

  while datetime.now().timestamp() < end_t:   # time.time() < end_t:
    curr_t = datetime.now().timestamp()       # time.time()
    _ = curr_t * curr_t

  end_t   =  datetime.now().timestamp         # time.time()

  # return ( end_t - start_t )                #  with just time.time()
  return ( datetime.now().timestamp() - start_t )      # didnt need timestamp-funciton with just time.time()

# ----- timers defined ---- 

_hidden_var = 42  # This is "private" by convention

def pf_get():
  global _hidden_var
  return _hidden_var

def pf_set():
  global _hidden_var
  _hidden_var = _hidden_var + 1 
  return _hidden_var

# test code, uncomment if testing

if __name__ == '__main__':

  print ( '\n --- start  : ', tmr_start(), '\t\t, this set the start-time.' )
  print (   ' --- set    : ', tmr_set()  , '\t\t, this set the lap-time stopwatch.' ) 

  print ( '\n --- dur    : ', tmr_durat(), '\t\t, this measured the stopwatch-time, very short.' )
  print (   ' --- tot    : ', tmr_total()  , '\t\t, this measured the total time since start, little longer.' )

  time.sleep ( 1 ) 
  print ( '\n --- dur1   : ', tmr_durat(), '\t\t, this measured the stopwatch-time, 1sec?.' )
  print (   ' --- tot1   : ', tmr_total(), '\t\t, this measured the total time since start, just over 1sec?' )

# print ( ' --- total3 : ', tmr_total() )
# print ( ' --- dur3   : ', tmr_durat() )
# print ( ' --- re-set : ', tmr_set() )
# print ( ' --- dur4   : ', tmr_durat() )

# time.sleep ( 1 ) 
# print ( '\n --- total4 : ', tmr_total() )
# print (   ' --- dur    : ', tmr_durat() )
  time.sleep ( 1) 
  print ( '\n --- re-set : ', tmr_set() )
  print (   ' --- dur0   : ', f" = {tmr_durat():9.5f}" )
  print (   ' --- total5 : ', f" = {tmr_total():9.5f}" )

  n_spin_sec = 3.14
  print ( '\n -- check spinning... ' )
  print (   ' --- re-set : ', tmr_set() )
  n_ret = tmr_spin ( n_spin_sec ) 
  print (   ' --- dur    : ', tmr_durat(), '\t\t, this measured the spin_time, ', n_spin_sec, ' sec?... ', n_ret , '.' )


  print ( ' -- testing pf -- ' )

  print ( 'pf_get : ', pf_get() ) 

  print ( ' - ' )
 
  print ( 'pf_set : ', pf_set() ) 

