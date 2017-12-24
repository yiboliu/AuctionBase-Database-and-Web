drop table if exists User;
drop table if exists Bid;
drop table if exists Category;
drop table if exists Item;
drop table if exists Buyer;
drop table if exists Seller;
create table User(
	userId varchar(100) primary key,
	rating float,
	location text,
	country varchar(100)
);
create table Seller(
	userId varchar(100) primary key,
	foreign key (userId) references User(userId)
);
create table Buyer(
	userId varchar(100) primary key,
	foreign key (userId) references User(userId)
);
create table Item(
	itemId varchar(100) primary key,
	sellerId varchar(100),
	startTime datetime,
	endTime datetime,
	firstBid float,
	currentBid float,
	numBid float,
	discription text,
	name varchar(100),
	foreign key (sellerId) references User(userId)
);
create table Category(
	itemId varchar(100),
	category varchar(100),
	primary key (itemId, category),
	foreign key (itemId) references Item(itemId)
);
create table Bid(
    buyerId varchar(100),
    itemId varchar(100),
    time datetime,
    price float,
    primary key(time, buyerId, itemId),
    foreign key(buyerId) references User(userID),
    foreign key(itemId) references Item(itemId)
);