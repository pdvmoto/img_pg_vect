

with i1 as ( 
select i.id, i.fname, v.img_vector
from vec_img i
   , vec_img_vect v
where v.img_id = i.id 
  and i.id > 2300
),
i2 as ( select i.id, i.fname, v.img_vector
from vec_img i
   , vec_img_vect v
where v.img_id = i.id 
  and i.id > 2300
)
select i1.fname, i2.fname
, to_char ( cosine_distance ( i1.img_vector, i2.img_vector), '0.00000') as cod_dist
from i1 i1, i2 i2
where i1.id < i2.id
order by (1- cosine_distance ( i1.img_vector, i2.img_vector)  ) ; 
