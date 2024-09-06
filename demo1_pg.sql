
-- pg: demonstrate vector with few elements, store and calculate distances.

drop table dv1 ; 

create table dv1 (
  id serial primary key
, vct vector(3)
) ; 

insert into dv1 (vct) values ('[1,2,3]'), ('[4,5,6]'), ('[1,1,1]');

-- simple distance to given element
SELECT id
, vct
, vct <-> '[2,3,4]'  as eucl_dist
, vct <=> '[2,3,4]'  as cos_dist
FROM dv1 
ORDER BY id ;


