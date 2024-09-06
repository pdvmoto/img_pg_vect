
-- need this table to combine vector-data into, 
-- sql on base-table didnt work ???

drop table vd2 ; 
CREATE TABLE vd2 (
    id      SERIAL PRIMARY KEY,
    fn1     text,
    fn2     text,
    vct1    VECTOR(2048),
    vct2    VECTOR(2048)
);


-- \echo now refresh the img data.
-- \echo .

insert into vd2 ( fn1, fn2         , vct1     , vct2 ) 
select img1.fname, img2.fname, img1.img_vector, img2.img_vector 
from img img1, img img2 
where img1.id < img2.id;

SELECT id, fn1, fn2,
       1 - (vct1 <=> vct2) AS cosine_similarity, -- cosine similarity
       vct1 <=> vct2 AS cosine_distance -- cosine distance
FROM vd2
where 1=1
order by 4 ;

\! echo -p "check that the two views are the similar images..." abc



