python  my-parser.py  ebay_data/items-*.json;
sort Item.dat | uniq > 1.dat;
sort User.dat | uniq > 2.dat;
sort Buyer.dat | uniq > 3.dat;
sort Seller.dat | uniq > 4.dat;
sort Bid.dat | uniq > 5.dat;
sort Category.dat | uniq > 6.dat;