select itemId 
from Item 
where currentBid = 
    (select max(currentBid) 
     from Item);