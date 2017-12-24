import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def transform_string(s):
    i = '\"'
    t = str(i + i)
    if i in s:
        ans = ""
        ss = s.split(i)
        for h in ss:
            ans += str(i + h + i)
        return ans
    else:
        return str(i+s+i)

def is_num(s):
    if s.isdigit():
        return True
    else:
        try:
            float(s)
            return True
        except:
            return False

def parseJson(json_file):
    Item = open("Item.dat", 'a')
    Category = open("Category.dat", 'a')
    Bidd = open("Bid.dat", 'a')
    User = open("User.dat", 'a')
    Buyers = open("Buyer.dat", 'a')
    Sellers = open("Seller.dat", 'a')
    Cats = open("Cats.dat", 'a')
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            temp = item
            its = transform_string(str(temp["ItemID"])) + "|" + transform_string(str(temp["Seller"]["UserID"])) + "|" + \
            transformDttm(str(temp["Started"])) + "|" + \
            transformDttm(str(temp["Ends"])) + "|" + \
            transformDollar(str(temp["First_Bid"])) + "|" + transformDollar(str(temp["Currently"])) + "|" + \
            str(temp["Number_of_Bids"]) + "|" + \
            transform_string(str(temp["Description"])) + "|" + transform_string(str(temp["Name"])) + '\n'
            Item.write(its)
            categories = temp["Category"]
            for cat in categories:
                c = transform_string(str(cat))
                Cats.write(c + '\n')
                Category.write(transform_string(str(temp["ItemID"])) + "|" + c + '\n')
            user = transform_string(str(temp["Seller"]["UserID"])) + "|" + str(temp["Seller"]["Rating"]) + "|" + \
            transform_string(str(temp["Location"])) + "|" + transform_string(str(temp["Country"])) + '\n'
            User.write(user)
            Sellers.write(transform_string(str(temp["Seller"]["UserID"])) + '\n')
            bids = temp["Bids"]
            if bids != None:
                for bid in bids:
                    b = transform_string(str(bid["Bid"]["Bidder"]["UserID"])) + "|" + transform_string(str(temp["ItemID"])) + "|" + \
                    str(bid["Bid"]["Time"]) + "|" + transformDollar(str(bid["Bid"]["Amount"])) + '\n'
                    Bidd.write(b)
                    user = transform_string(str(bid["Bid"]["Bidder"]["UserID"])) + "|" + \
                    str(bid["Bid"]["Bidder"]["Rating"]) + "|"
                    if "Location" in bid["Bid"]["Bidder"].keys():
                        user += transform_string(bid["Bid"]["Bidder"]["Location"])
                    else:
                        user += 'NULL'
                    user += "|"
                    if "Country" in bid["Bid"]["Bidder"].keys():
                        user += transform_string(bid["Bid"]["Bidder"]["Country"])
                    else:
                        user += 'NULL'
                    user += '\n'
                    User.write(user)
                    Buyers.write(transform_string(str(bid["Bid"]["Bidder"]["UserID"])) + '\n')
    Item.close()
    Category.close()
    Bidd.close()
    User.close()
    Buyers.close()
    Sellers.close()



"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
