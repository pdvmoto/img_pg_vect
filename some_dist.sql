

with 
i1 as ( select i.id, i.fname, v.img_vector
from vec_img i
   , vec_img_vect v
where v.img_id = i.id 
--  and i.id > 0
),
i2 as ( select i.id, i.fname, v.img_vector
from vec_img i
   , vec_img_vect v
where v.img_id = i.id 
--  and i.id > 0
)
select i1.fname, i2.fname
, to_char (     vector_distance ( i1.img_vector, i2.img_vector), '0.00000') as cos_dist
, to_char ( 1 - vector_distance ( i1.img_vector, i2.img_vector), '0.00000') as cos_simil
from i1 i1, i2 i2
where i1.id < i2.id
-- and (  cosine_distance ( i1.img_vector, i2.img_vector)  < 0.01
--     or cosine_distance ( i1.img_vector, i2.img_vector)  > 0.9
--     )
order by i1.id -- cosine_distance ( i1.img_vector, i2.img_vector)  ; 
;
