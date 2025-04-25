#
# ora_login.py: , using .env, dotenv, and return the connection.
# another way of isolating the logon cred + avoid typing code
#
# todo: 
# - later: allow un/pwd@host:port\sid to be passed, but prefer dotenv 
# - how many other self-made includes should I depend on ? 
# 
import    os
import    oracledb
from      dotenv   import load_dotenv


# define function to have any arguments, 
# this allow to replace existing functions. 

def ora_logon ( *args ):

  # customize this sql to show connetion info on logon
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
              , '98b6d46dd637',    ' (xe-dev)'
              , '98eac28a59c0',    ' (dckr-23c)'
              , '2c4a51017a44',    ' (dckr-23ai)'
              , ' (-envname-)')
         || ' > '
    FROM    v$database      db
  order by 1
  """

  # --- dotenv() specific --- ----------------------------
  # --- but feel free to code your own "credentials" here.

  load_dotenv()

  # get + verify..
  ora_user    = os.getenv ( 'ORA_USER' )
  ora_pwd     = os.getenv ( 'ORA_PWD' )
  ora_server  = os.getenv ( 'ORA_SERVER' )
  ora_port    = os.getenv ( 'ORA_PORT' )
  ora_sid     = os.getenv ( 'ORA_SID' )

  # --- dotenv() specific ------------------------------

  # 
  # verify... dont print this at work.
  print    ( ' ora_login: ' ) 
  print    ( ' ora_login: ' + ora_user + ' / **************** @ ' 
           + ora_server + ' ; ' + ora_port + ' \\ ' + ora_sid )

  # create the actual connection
  ora_conn = oracledb.connect (
      user          = ora_user
    , password      = ora_pwd
    , host          = ora_server
    , port          = ora_port
    , service_name  = ora_sid
  )

  print    ( ' ora_login: --- Connection is: --->' )

  cursor = ora_conn.cursor()
  for row in cursor.execute ( sql_show_conn ):
    print  ( ' ora_login:', row[1] )

  print    ( ' ora_login:  <-- Connection  ---- ' )
  print    ( ' ora_login: ' ) 

  return ora_conn  # ------- logon and return conn object --- 


def ora_sess_info ( the_conn ):
  # 
  # output network and other stats from session 
  # 
  sql_stats = """
    select sn.name, st.value
    --, st.* 
    from v$mystat st
    , v$statname sn
    where st.statistic# = sn.statistic# 
    and (  sn.name like '%roundtrips%'
        or sn.name like 'bytes sent%client'
        or sn.name like 'bytes rece%client'
        or sn.name like '%execute count%'
        or sn.name like 'user calls'
        or sn.name like 'user commits'
        or sn.name like 'user rollbacks'
        or sn.name like 'consistent gets'
        or sn.name like 'db block gets'
        or sn.name like 'opened cursors current'
        or sn.name like 'opened cursors curr%'
        or sn.name like '%sorts%'
        or sn.name like '%physical reads'
        )
      order by sn.name 
  """

  print ( ' ora_sess_info: Report out Session Stats ' ) 

  cur_stats = the_conn.cursor()
  for row in cur_stats.execute ( sql_stats ):
    # p   ( ' stats : ', row[1], ' ', row[0] )
    print   ( ' ora_sess_info: ', f"{row[1]:10d}  {row[0]}"   )

  return 0 # -- -- -- -- ora_sess_info


# ---- some  test code below... ---- 

sql_test = """
  select object_type, count (*) 
    from user_objects 
   group by object_type  
"""

if __name__ == '__main__':

  print ()
  print ( ' ---- testing ora_logon function ----- ' )
  print ()

  ora_conn = ora_logon ()

  print ()
  print ( ' ---- if connected, test a query ----- ' )
  print ()

  cur_logon = ora_conn.cursor ()
  for row in cur_logon.execute ( sql_test ):
    print ( ' ora_logon:', row ) 
  
  print ()
  print ( ' ---- ora_logon: tested with count * for user_objects ---- ' ) 
  print ()

  ora_sess_info ( ora_conn )

  print ()
  print ( ' ---- ora_sess_info: tested with current session ---- ' ) 
  print ()

