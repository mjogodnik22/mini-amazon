import csv
import random



#Products

objAdj = ['Slow', 'Squeaky', 'Clean', 'Gently Used', 'Enormous', 'Miniscule']
personAdj = ['Slimy', 'Great', 'Horrible', 'Generous', 'Rude']
nouns = ['Paper Towels', 'Kind Bars', 'Dyson Microwave', 'Snowshoes', 'Champion Hoodie']
categories = ['Essentials', 'Food', 'Clothes', 'Electronics', 'Outdoor']
potStatus = ['Fulfilled', 'Not Fulfilled']
firstNames = ['Gogo', 'Pogo', 'Togo', 'Shogo', 'Logo']
lastNames = ['Gadget', 'Power', 'Toulousse', 'Lowry', 'Sheveries']
dates = ['2018-09-06 10:00:00','2018-10-31 13:00:00','2019-10-31 18:00:00','2020-10-31 18:00:00','2020-02-22 07:00:00']

with open('Users.csv', 'w', newline='') as users, open('HashedPasswords.csv', 'r', newline='') as pwd:
	#Users: uid, email, pass, firstname, lastname, address, balance
	uWriter = csv.writer(users)
	pwdReader = csv.reader(pwd)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		password = pwdReader.__next__()[0]
		email = 'email{}@gmail.com'.format(i)
		firstName = random.choice(firstNames)
		lastName = random.choice(lastNames)
		addr = '10{} Downey Street'.format(i)
		bal = round(random.uniform(2000, i+2000), 2)
		uWriter.writerow([uid, email, password, firstName, lastName, addr, bal])
	
with open('Products.csv', 'w', newline='') as prods:
	#Products: pid, sid, name, desc, category, pic, price, quantity
	pWriter = csv.writer(prods)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		pid = i + 100

		itemDesc = random.choice(objAdj)
		objName = itemDesc + ' ' + random.choice(nouns)
		price = round(random.uniform(0,i), 2)
		quant1 = random.randint(2,i+2)+2
		pData = [pid, uid, objName, "Very "+ itemDesc, random.choice(categories), '/static/images/paper_towel.jpg', price, quant1]
		pWriter.writerow(pData)






with open('Sellers.csv', 'w', newline='') as sellers:
	sWriter = csv.writer(sellers)
	for i in range(1, 2001):
		uid = i
		sWriter.writerow([i])
	
	
with open('OrderInformation.csv', 'w', newline='') as ordInfo:
	#OrderInformation: oid, uid, date
	oiWriter = csv.writer(ordInfo)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		oid = i + 1000
		date = random.choice(dates)
		oiWriter.writerow([oid, uid, date])

with open('ItemsInOrder.csv', 'w', newline='') as itemsInOrd:
	#ItemsInOrder: oid, pid, quantity2, price, status
	iioWriter = csv.writer(itemsInOrd)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		pid = i + 100
		pidOrdered = (pid + 1)
		if pidOrdered > 2100:
			pidOrdered = (pidOrdered%2100)+100
		oid = i + 1000
		status = random.choice(potStatus)
		quant2 = random.randint(1, random.randint(2,i+2))
		iioWriter.writerow([oid, pidOrdered, quant2, price, status])

with open('ProductReview.csv', 'w', newline='') as prodRev:
	#ProductReview: uid, pid, rating, desc
	prWriter = csv.writer(prodRev)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		pid = i + 100
		pidOrdered = (pid + 1)
		if pidOrdered > 2100:
			pidOrdered = (pidOrdered%2100)+100
		pRating = random.randint(1,5)
		pDesc = " ".join(random.sample(objAdj, 2))
		prWriter.writerow([uid, pidOrdered, pRating, pDesc])
		
with open('SellerReview.csv', 'w', newline='') as slrRev:
	#SellerReview: uid (buyer), uid(seller), rating, review
	srWriter = csv.writer(slrRev)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		pid = i + 100
		pidOrdered = (pid + 1)
		if pidOrdered > 2100:
			pidOrdered = (pidOrdered%2100)+100
		oid = i + 1000
		sRating = random.randint(1,5)
		sRev = " ".join(random.sample(objAdj, 2)) + " seller!!"
		srWriter.writerow([uid, (uid+1)%2000, sRating, sRev])

with open('Carts.csv', 'w', newline='') as carts:
	#Carts: uid, pid, quantity3
	ctsWriter = csv.writer(carts)
	for i in range(1, 2001):
		random.seed(i)
		uid = i
		pid = i + 100
		pidOrdered = (pid + 1)
		if pidOrdered > 2100:
			pidOrdered = (pidOrdered%2100)+100
		oid = i + 1000
		ctsWriter.writerow([uid, pidOrdered, random.randint(1, 2)])	