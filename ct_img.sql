
-- original table, with array or double
create table image_features (
  id              serial primary key
, image_name      text              
, feature_vector  double precision[] 
) ; 


-- try vector to allow vector-logic
create table img (
 id       serial primary key
, filename  text  
, img_vct   VECTOR(2048)
) ; 
