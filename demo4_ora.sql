
column id         format 9999 
column id1        format 9999 
column id2        format 9999 
column fn1        format A20 
column fn2        format A20 
column fname      format A20
column cos_sim    format 9.999999 
column openstmnt  format A80

set echo on
create or replace view img_compare as (
select i1.id      id1
     , i1.fname   fn1
     , i2.id      id2
     , i2.fname   fn2 
     , ( 1.0 - (v2.img_vector   <=> v1.img_vector ) ) COS_SIM
from vec_img      i1, vec_img      i2
   , vec_img_vect v1, vec_img_vect v2
where v1.img_id = i1.id
  and v2.img_id = i2.id
);

-- test right away, on small set...
select id1, fn1, id2, fn2, cos_sim 
from img_compare 
where 1=1
  and id2 < 200
  and id1 < id2
  and cos_sim > 0.8
order by cos_sim ;

set echo off
! read -p "view created to join images And Calculate cos_sim"
set echo on

create or replace view img_compare as ( 
select i1.id         id1
     , i1.fname      fn1 
     , i2.id         id2
     , i2.fname      fn2
  , ( 1.0 - (v2.vect  <=> v1.vect ) ) cos_sim
from img_file   i1, img_file    i2
   , img_vector v1, img_vector  v2
where v1.img_file_id = i1.id
  and v2.img_file_id = i2.id
);

set echo off
! read -p "view created to join images And Calculate cos_sim"
set echo on


-- test right away, on small set...
select id1, fn1, id2, fn2, cos_sim 
from img_compare 
where 1=1
  and id2 < 200
  and id1 < id2
  and cos_sim > 0.8
order by cos_sim ;

set echo off
! read -p "view created to join images And Calculate cos_sim

create or replace view img_compare as ( 

select id, fname from vec_img where fname like '%view%' order by id ;

select i1.id, i2.id
  , ( 1.0 - (v2.img_vector   <=> v1.img_vector ) ) cos_sim
from vec_img      i1, vec_img      i2
   , vec_img_vect v1, vec_img_vect v2
where v1.img_id = i1.id
  and v2.img_id = i2.id
  and i1.fname like '%view%'
  and i1.id > i2.id -- prevent doubles
  and ( 1.0 - (v2.img_vector   <=> v1.img_vector ) ) > 0.4
order by i1.id, i2.id
;

select id, fname , fullpath from img_file where id in ( 7, 289, 9046, 174, 927 ) order by id ;

select i1.id, i1.fname, i2.id, i2.fname
  , ( 1.0 - (v2.vect  <=> v1.vect ) ) cos_sim
from img_file   i1, img_file    i2
   , img_vector v1, img_vector  v2
where v1.img_file_id = i1.id
  and v2.img_file_id = i2.id
  and i1.id = 7 
  -- and i1.fname like '%20220622_0840331%'
  and i1.id < i2.id -- prevent doubles
  and ( 1.0 - (v2.vect   <=> v1.vect ) ) between 0.9 and 1.0 
order by 5, i1.id, i2.id
;

set echo on

select id1, fn1, id2, fn2, cos_sim 
from img_compare 
where id1 = 7
  and cos_sim > 0.9
order by cos_sim ;

set echo off
! read -p "images similar to id=7, should be pylons" abc 
set echo on

select '! open '|| fullpath as openstmnt
from img_file where id in ( 7, 289, 9046, 174, 927 ) 
order by id ;


