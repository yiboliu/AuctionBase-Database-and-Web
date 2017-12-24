select count(itemId) 
from Item  
where itemId in (select itemId from Category group by itemId having count(itemId) = 4);