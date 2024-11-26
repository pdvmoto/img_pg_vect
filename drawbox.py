
import time
from datetime import datetime 

from PIL import Image, ImageDraw

# need functions:
# - tmr_start() : set start point, return now()    global variable: g_start_total
# - tmr_total() : get sec since tmr_total, stopwatch from start of program
# - tmr_set()   : set point to measure, now(), also re-sset.. global_var: g_start_dur
# - tmr_durat() : get duration in sec/ms since last set, the stopwatch inside the program
# 
# todo: use more than 1 timer..so they dont interfere. allow nested timeing
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

# ----- timers defined ---- 

# test code
print ( ' --- start  : ', tmr_start() )
print ( ' --- set    : ', tmr_set() )
print ( ' --- dur    : ', tmr_durat() )

time.sleep ( 0.5 ) 
print ( ' \n --- dur    : ', tmr_durat() )
print ( ' --- total  : ', tmr_total() )
print ( ' --- dur2   : ', tmr_durat() )
print ( ' --- total2 : ', tmr_total() )
print ( ' --- total3 : ', tmr_total() )
print ( ' --- dur3   : ', tmr_durat() )
print ( ' --- re-set : ', tmr_set() )
print ( ' --- dur4   : ', tmr_durat() )

time.sleep ( 0.5 ) 
print ( '\n --- total4 : ', tmr_total() )
print (   ' --- dur    : ', tmr_durat() )
time.sleep ( 1) 
print ( '\n --- re-set : ', tmr_set() )
print (   ' --- dur0   : ', f" = {tmr_durat():9.5f}" )
print (   ' --- total5 : ', f" = {tmr_total():9.5f}" )


print ( '\n --- timer-re-set : ', tmr_set() )

fullpath = '/Users/pdvbv/zz_imgs/2_view.jpg'

l_img = Image.open ( fullpath  )

img_width, img_height = l_img.size

x1 = img_width / 4 
x2 = x1 + ( img_width / 2 )

y1 = img_height / 4 
y2 = y1 + ( img_height / 2 )

l_color_red = ( 255, 0,0 )

print (   ' --- opened, elapsed  : ', f" = {tmr_durat():9.5f} sec" )

l_img.show ()

print (   ' --- shown, elapsed   : ', f" = {tmr_durat():9.5f} sec" )

# make draw-object + work on it

tmr_set()

# draw works on the local image, still l_img
l_draw = ImageDraw.Draw ( l_img ) 
l_draw.rectangle([x1, y1, x2, y2], outline=l_color_red, width=4)

print (   ' --- drawn, elapsed   : ', f" = {tmr_durat():9.5f} sec" )

l_img.show()

print (   ' --- re-shown, elapsed   : ', f" = {tmr_durat():9.5f} sec" )

