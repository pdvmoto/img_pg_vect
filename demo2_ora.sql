
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

-- check raw data..
select i.id, i.fname, v.img_vector
from vec_img i, vec_img_vect v 
where i.id = v.img_id
order by i.id ; 

-- now the distances..
select id, fn1, fn2, 
       1 - (vct1 <=> vct2) AS cosine_similarity, -- cosine similarity
       vct1 <=> vct2 AS cosine_distance -- cosine distance
from vd2
where 1=1
order by 1  ; 

! echo .
! read -p "cosine-dist, with 1_view.jpg and 2_view.jpg nearly identical \n.." abc

select id, fn1, fn2, 
       vector_distance ( vct1,vct2, COSINE          )  cos_d ,
       vector_distance ( vct1,vct2, EUCLIDEAN       )  eucl_d ,
       vector_distance ( vct1,vct2, MANHATTAN       )  mahat_d 
from vd2
where 1=1
order by 1  ; 

select id, fn1, fn2, 
       vector_distance ( vct1,vct2, COSINE          )  cos_d ,
       vector_distance ( vct1,vct2, EUCLIDEAN       )  eucl_d ,
       vector_distance ( vct1,vct2, MANHATTAN       )  mahat_d 
from vd3
where 1=1
order by 1  ; 


select id, img_id
, vector_dimension_count ( img_vector ) 
, vector_dimension_format ( img_vector ) 
from vec_img_vect 
order by id  ;
