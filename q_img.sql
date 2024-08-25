
select img1.filename file1, img2.filename file2
, img1.img_vct <==> img2.img_vct as cos_dist
from img img1, img img2
order by 3 ; 

