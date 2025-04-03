
-- rt1.sq: for use with round trip measurements 

--
-- need a small table (cache) to hold data, and use it for retrieval to observe  latence
-- 
-- probably separate two types of retrieval: atomic (small) or array (large...)
--



drop table rt1 ;

create table if not exists rt1 (
  id INTEGER GENERATED ALWAYS AS IDENTITY 
, payload varchar2(1024) 
, PRIMARY KEY (id) ) ; 

-- later: created_dt..

insert into rt1 ( payload)
select DBMS_RANDOM.STRING('X', 512) from dual connect by level <= 100000 ; 

select count (*) from rt1;



