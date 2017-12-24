select count(UserID) from Seller
where UserID in (select UserID from Buyer);