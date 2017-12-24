select count(distinct(category)) 
from Category 
where itemId in 
    (select distinct(itemId) 
     from Bid
     group by itemId 
     having max(price)>100 and max(price)<>'NULL');