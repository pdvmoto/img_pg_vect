# inspect a python object:
# show type, dir, length, rep, and more..
# ------------------------------------------------

# this prefix seems to remain local to functions in the file?

def f_prfx():
  return "inspect_obj: "

def f_inspect_obj( s_objname, o_obj ):

  print ( f_prfx(), "-------- Object :", s_objname, "--------" )

  print ( f_prfx(), "o_obj -[", o_obj, "]-" )
  print ( f_prfx(), "o_obj type  : ",  type (o_obj ) )

  if o_obj != None:

    print ( f_prfx(), "o_obj length: ",  len (o_obj ) )
    print ( f_prfx(), "o_obj dir   : ",  dir (o_obj ) )
    print ( " " )
    # hit_enter = input ( f_prfx() + "meta data from " + s_objname + "...., hit enter.." )

    print ( "--- repr --->" )
    print ( f_prfx(), "o_obj repr  : ",  repr ( o_obj ) )
    print ( "<--- repr ---  " )

  # only if obj is not empty

  print ( f_prfx(), " ------ inspected o_obj ", s_objname, " ---------- " )
  hit_enter = input ( f_prfx() + "about to go back...., hit enter.." )

# end of f_inspect_obj, show properties of an object

