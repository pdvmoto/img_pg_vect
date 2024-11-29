
-- better search, by exclusing..

set linesize 100 

column caption_txt    format a70 
column file_id        format 99999 
column fname          format A25

set echo on

-- the simple one.


select caption_txt, count (*) from img_caption group by caption_txt order by 2 ; 

! read total_hitenter

-- leave out the moto
select caption_txt, count (*) 
from img_caption 
where caption_txt not like '%motorcycle%'
  and 0  
group by caption_txt 
order by 2 ; 

! read no_moto

select caption_txt, count (*) 
from img_caption 
where caption_txt like '%motorcycle%'
  and 0  
group by caption_txt 
order by 2 ; 

select 'total_moto', count (*) 
from img_caption 
where caption_txt like '%motorcycle%'
  and 0  
group by 'total_moto' 
order by 2 ; 

! read moto_references

select caption_txt, count (*) 
from img_caption 
where caption_txt like '%metal object%hole%'
  and 0  
group by caption_txt 
order by 2 ; 

! read oil_check

-- the clean one
select caption_txt, count (*) 
from img_caption 
where caption_txt not like '%motorcycle%'
  and caption_txt not like '%himself%'
  and caption_txt not like '%woman%'
  and 0  
group by caption_txt 
order by 2 ; 

! read cleanlist 

-- the funny  one
select caption_txt, count (*) 
from img_caption 
where length (caption_txt) > 80
  and caption_txt not like '%letter%'
  and 0  
group by caption_txt 
order by 2 ; 

! read funnylist 

select ic.caption_txt
     , if.id as file_id
     , if.fname  
from img_caption ic
   , img_file if
where if.id in ( 7, 174, 289, 927, 9046 )
  and ic.img_file_id = if.id
order by if.id
;

! read pylons_surprise

-- searhing
select caption_txt, count (*) 
from img_caption 
where 1=1
  and caption_txt like '%a vase filled with flowers on top of a table%'
group by caption_txt 
order by 2 ; 

! read searchvase 

-- searhing
select ic.caption_txt, if.fname
from img_caption  ic
   , img_file     if
where if.id < 1300
  and if.id = ic.img_file_id
order by 2 desc ; 

! read searchvase 


