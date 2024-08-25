
CREATE TABLE vector_data (
    id SERIAL PRIMARY KEY,
    vector1 VECTOR(3),
    vector2 VECTOR(3)
);

CREATE TABLE vd2 (
    id SERIAL PRIMARY KEY,
    fn1     text,
    fn2     text,
    vct1 VECTOR(2048),
    vct2 VECTOR(2048)
);

INSERT INTO vector_data (vector1, vector2)
VALUES
  ('[0.1, 0.2, 0.3]', '[0.4, 0.5, 0.6]'),
  ('[0.7, 0.8, 0.9]', '[0.1, 0.2, 0.3]');

INSERT INTO vd2 (vector1, vector2)
VALUES
  ('[0.1, 0.2, 0.3]', '[0.4, 0.5, 0.6]'),
  ('[0.7, 0.8, 0.9]', '[0.1, 0.2, 0.3]');

SELECT id, 
       1 - (vector1 <=> vector2) AS cosine_similarity, -- cosine similarity
       vector1 <=> vector2 AS cosine_distance -- cosine distance
FROM vector_data;

SELECT id, 
       1 - (vector1 <=> vector2) AS cosine_similarity, -- cosine similarity
       vector1 <=> vector2 AS cosine_distance -- cosine distance
FROM vd2;

insert into vd2 ( fn1, fn2         , vct1     , vct2 ) 
select img1.filename, img2.filename, img1.img_vct, img2.img_vct 
from img img1, img img2 ;

SELECT id, fn1, fn2,
       1 - (vct1 <=> vct2) AS cosine_similarity, -- cosine similarity
       vct1 <=> vct2 AS cosine_distance -- cosine distance
FROM vd2
order by 4 ;

