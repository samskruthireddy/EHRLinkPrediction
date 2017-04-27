
use umls2016ab;
select  distinct b.CODE,
                 b.STR3,
                 a.RELA,
                 c.CODE,
                 c.STR1
from
(select distinct CUI1,RELA,CUI2 from MRREL where CUI1 in (select distinct CUI from MRCONSO where SAB="ICD9CM") and
CUI2  in (select distinct CUI from MRCONSO where SAB="ICD9CM") and RELA is not null and CUI1 != CUI2) as a
join  (select CUI,STR as STR3,CODE from MRCONSO where SAB="ICD9CM" and LAT="ENG" ) as b
on a.CUI1=b.CUI
join (select CUI,STR as STR1,CODE from MRCONSO where SAB="ICD9CM" and LAT="ENG") as c
on a.CUI2=c.CUI
INTO OUTFILE '/var/lib/mysql/withicd9.txt'
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
