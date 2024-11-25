
-- demo6_ora.. 

select i1.id, i2.id, i1.fname, i2.fname  
    ,  1 - vector_distance ( i1.img_vector, i2.img_vector, COSINE )  cos_sim_fn
    ,  1 - ( i1.img_vector <=> i2.img_vector  )                     cos_sim_op
from img i1, img i2
where i1.id < i2.id
order by 5 ;
