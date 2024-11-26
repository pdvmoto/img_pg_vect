
import sys
from datetime import datetime

# take the filename, to use as prefix for print stmnts
#pyfile = os.path.basename(__file__)
arg0 = sys.argv[0] 
pyfile = sys.argv[0] 

def f_prfx():
  # set a prefix for debug-output, sourcefile + timestamp

  s_timessff = str ( datetime.now() )[11:23]
  s_prefix = pyfile + ' ' + s_timessff + ': '

  # print ( prfx, ' in function f_prfx: ' , s_prefix )

  return str ( s_prefix )

# ---- end of f_prfx, set sourcefile and timestamp ----

def pp ( *argv ):
  print ( f_prfx(), ' : ',  *argv )
  return 0   # consider returning nr-args, or length of string



print ( '[', f_prfx(), ']') 

