select count(UserID) from User
where UserID in (select * from Seller)
and rating > 1000;