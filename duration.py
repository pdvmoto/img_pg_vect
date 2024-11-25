
from datetime import datetime 

# need functions:
# - tmr_start() : set start point, return epoch (sec)
#                           global variable: g_start_total
# - tmr_total() : sec + ms since start_total
# - tmr_set()   : set point to measure, now(), also re-sset..
#                           global_var: g_start_dur
# - tmr_dur()   : get duration in sec/ms since last set
# 
# todo: use more than 1 timer..so they dont interfere. allow nested timeing
#

# ----- timers here ---- 

# define global vars, of type now()
g_tmr_total = datetime.now()
g_tmr_durat = datetime.now()

def tmr_start ():
  g_tmr_total = datetime.now()
  return g_tmr_total  # later: insert epoch-seconds..  

def tmr_set ():
  g_tmr_durat = datetime.now()
  return g_tmr_durat   # lter: insert epoch timer

def tmr_total ():
  ela = ( datetime.now() - g_tmr_total ).total_seconds()
  return  ela

def tmr_dur ():
  durat = ( datetime.now() - g_tmr_durat ).total_seconds()
  return  durat

# ----- timers defined ---- 

# test code
print ( ' --- start : ', tmr_start() )
print ( ' --- set   : ', tmr_set() )
print ( ' --- dur   : ', tmr_dur() )
print ( ' --- total : ', tmr_total() )

print ( ' --- dur2   : ', tmr_dur() )
print ( ' --- total2 : ', tmr_total() )


print ( ' --- re-set: ', tmr_set() )
print ( ' --- total : ', tmr_total() )
print ( ' --- dur   : ', tmr_dur() )

