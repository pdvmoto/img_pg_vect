
-- demo3_ora.sql: demo tables for cos-dist

/*  */ 
drop table tv ; 
/* */

-- store image, just the jpg/blob and remarks.
-- consider attributes : img-type, img_size.. 
create table tv ( 
  id            NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  created_dt    date                default sysdate,
  fname         VARCHAR2(255),
  remarks       VARCHAR2(255), 
  img_vector    VECTOR (2048, FLOAT32 ) 
);

-- copy some existing vectors
-- insert into tv ( fname, img_vector ) select id, img_vector from vec_img_vect ;

! echo .
! echo " Now insert some simple arrays via python to verify calculations "
! echo .
! read " Run   python3 p4.py   and check results.. " abc

select v1.id, v1.fname 
     , v2.id, v2.fname
     ,  vector_distance ( v1.img_vector,v2.img_vector, COSINE          )  cos_d 
     ,  vector_distance ( v1.img_vector,v2.img_vector, EUCLIDEAN       )  eucl_d 
     ,  vector_distance ( v1.img_vector,v2.img_vector, MANHATTAN       )  mahat_d
from tv v1, tv v2
where 1=1
  and v1.id < v2.id
order by v1.id ; 

select i1.id, i2.id, i1.fname, i2.fname  
    ,  1 - vector_distance ( v1.img_vector,v2.img_vector, COSINE )  cos_sim_fn
    ,  1 - ( v1.img_vector <=> v2.img_vector  )                     cos_sim_op
from img i1, imd i2
where i1.id < i2.id
order by i1.id;
