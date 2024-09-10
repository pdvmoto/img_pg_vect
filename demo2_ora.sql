
-- create views to get code indentical to other demo

drop view vd2 ; 
create view vd2 as (
select v1.id
     , i1.fname as fn1
     , i2.fname fn2
     , v1.img_vector as vct1
     , v2.img_vector as vct2
from vec_img i1
   , vec_img i2
   , vec_img_vect v1
   , vec_img_vect v2
where 1=1
  and i1.id = v1.img_id
  and i2.id = v2.img_id
  and i1.id < i2.id
) ; 

-- test with copy of data, this helped in pg16
drop table vd3;
create table vd3 as 
select v1.id
     , i1.fname as fn1
     , i2.fname fn2
     , v1.img_vector as vct1
     , v2.img_vector as vct2
from vec_img i1
   , vec_img i2
   , vec_img_vect v1
   , vec_img_vect v2
where 1=1
  and i1.id = v1.img_id
  and i2.id = v2.img_id
  and i1.id < i2.id
 ; 

drop view vd4 ; 
create view vd4 as (
select i1.id id1
     , i2.id id2
     , i1.img_vector as vct1
     , i2.img_vector as vct2
from img i1
   , img i2
where 1=1
  and i1.id < i2.id
) ; 

-- check raw data..
select i.id, i.fname, v.img_vector
from vec_img i, vec_img_vect v 
where i.id = v.img_id
order by i.id ; 

select id, img_vector
from img
order by id ;

! echo .
! read -p "check raw data from vec_img_vect and img ... " abc

-- set timing on

-- now the distances..
select id, fn1, fn2, 
       1 - (vct1 <=> vct2) AS cos_sim, -- cosine similarity
       vct1 <=> vct2 AS cos_d, -- cosine distance
       vct1 <-> vct2 AS ucl_d -- euclidian distance
from vd2
where 1=1
order by 4  ; 

! echo .
! read -p "cos, eucl dist, using uperators on view vd2... " abc

select id, fn1, fn2, 
       vector_distance ( vct1,vct2, COSINE          )  cos_d ,
       vector_distance ( vct1,vct2, EUCLIDEAN       )  eucl_d ,
       vector_distance ( vct1,vct2, MANHATTAN       )  mahat_d 
from vd2
where 1=1
order by 4 desc ; 

! echo .
! read -p "vector_dist using functions on vd2... " abc

select id, '! open ' || fn1, '! open ' || fn2, 
       vector_distance ( vct1,vct2, COSINE          )  cos_d ,
       vector_distance ( vct1,vct2, EUCLIDEAN       )  eucl_d ,
       vector_distance ( vct1,vct2, MANHATTAN       )  mahat_d 
from vd3
where 1=1
order by 4 desc  ; 

! echo .
! read -p "vector_dist calculated from table vd3, nearly identical \n.." abc

-- try using plsql..

set serveroutput on 

declare 
  n number ;
begin

  for cur in ( select id, lpad ( fn1, 20 ) fn1 , lpad (fn2, 20 ) fn2 ,
               to_char ( vector_distance ( vct1,vct2, COSINE          ), '9.99999' )  cos_d ,
               to_char ( vector_distance ( vct1,vct2, EUCLIDEAN       ), '9.99999' )  eucl_d ,
               to_char ( vector_distance ( vct1,vct2, MANHATTAN       ), '9.99999' )  mahat_d
        from vd3
        where 1=1
        order by 4 desc  ) loop

    dbms_output.put_line ( 'id: ' || cur.id || ' fns: ' || cur.fn1 || ' ' || cur.fn2 || ' cos_d: ' || cur.cos_d ) ; 

  end loop ; -- end cur

  for cur in (  select id, lpad ( fn1, 20 ) fn1, lpad ( fn2, 20 ) fn2,
       to_char ( 1 - ( vct1 <=> vct2 ) ,   '999.999999' )  AS cos_sim,
       to_char (     ( vct1 <-> vct2 ) ,   '999.999999' )  AS ucl_d 
    from vd2
    where 1=1 
    order by 4 ) loop

    dbms_output.put_line ( 'id: ' || cur.id || ' fns: ' || cur.fn1 || ' ' || cur.fn2 
                        || ' cos_sim: ' || cur.cos_sim 
                        || ' ucl_d: ' || cur.ucl_d 
                       ) ; 

  end loop ; -- second cursor

end;
/

! echo .
! read -p "distances using plsql on vd3 and vd2 \n.." abc


select id1, id2,  1 - vector_distance ( vct1,vct2, COSINE          )  cos_sim 
from vd4 
order by id1, id2 ; 

select id1
, ( 1 - ( vct1 <=> vct2 ) ) as cos_sim 
, ( 1 - ( vct1 <-> vct2 ) ) as cos_sim 
, ( 1 - ( vct1 <#> vct2 ) ) as cos_sim 
from vd4 ;

! echo .
! read -p "distances on vd4, from img  \n.." abc


/* 
select id, img_id
, vector_dimension_count ( img_vector ) 
, vector_dimension_format ( img_vector ) 
from vec_img_vect 
order by id  ;
*/

