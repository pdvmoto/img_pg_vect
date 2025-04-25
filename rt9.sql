
-- rt9.sq: for use with round trip measurements , expt looong table

--
-- need a long table (cache) to fetch many records
-- 
--



drop table rt9 ;

create table if not exists rt9 (
  id INTEGER GENERATED ALWAYS AS IDENTITY 
, payload varchar2(1024) 
, PRIMARY KEY (id) ) ; 

-- later: created_dt..

insert into rt9 ( payload)
select DBMS_RANDOM.STRING('X', 16) from dual connect by level <= 1000000 ; 
/
/
/
/

select count (*) from rt9;

