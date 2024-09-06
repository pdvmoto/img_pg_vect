
drop table img ;

-- try vector to allow vector-logic
create table img (
  id        serial primary key
, fpath     text  
, fname     text  
, img_data  bytea 
, img_vector VECTOR(2048)
) ; 

-- drop table vec_img ; 
-- drop table image_features ; 

-- original table, with array or double
-- create table image_features (
--  id              serial primary key
--, image_name      text              
--, feature_vector  double precision[] 
--) ; 

