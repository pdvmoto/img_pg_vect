
-- rt1.sq: for use with round trip measurements 

--
-- need a small table (cache) to hold data, and use it for retrieval to observe  latence
-- 
-- probably separate two types of retrieval: atomic (small) or array (large...)
--



drop table rt2 ;

create table if not exists rt2 (
  id INTEGER GENERATED ALWAYS AS IDENTITY 
, payload1 varchar2(4000) 
, payload2 varchar2(4000) 
, PRIMARY KEY (id) ) ; 

-- later: created_dt..

insert into rt2 ( payload1, payload2)
select DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512) 
,   DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
||  DBMS_RANDOM.STRING('X', 512)  
from dual connect by level <= 100000 ; 

select count (*) from rt2;



