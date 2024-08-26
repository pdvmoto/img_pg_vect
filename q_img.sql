
-- Why doesnt this work ???
select i1.filename file1, i2.filename file2
, i1.img_vct <==> i2.img_vct as cos_dist
from img i1, img i2
 ; 

-- this dosnt work eiher.. something with the img table def ? 
select img.filename, vd2.fn2
     , img.img_vct <==> vd2.vct2 as cos_dist
from img, vd2
where img.filename = vd2.fn1 ;

select img.filename, vd2.fn1, vd2.fn2
     , vd2.vct1 <==> vd2.vct2 as cos_dist
from img, vd2
where img.filename = vd2.fn1 ;
