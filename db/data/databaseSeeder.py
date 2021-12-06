import csv
import random
from faker import Faker
from faker.providers import internet, misc, lorem, date_time, profile
from werkzeug.security import generate_password_hash


#Products

objAdj = ['Slow', 'Squeaky', 'Clean', 'Gently Used', 'Enormous', 'Miniscule']
personAdj = ['Slimy', 'Great', 'Horrible', 'Generous', 'Rude']
nouns = ['Paper Towels', 'Kind Bars', 'Dyson Microwave', 'Snowshoes', 'Champion Hoodie']
categories = ["Appliances", "Apps & Games","Arts, Crafts, & Sewing","Automotive Parts & Accessories","Baby","Beauty & Personal Care","Books","CDs & Vinyl","Cell Phones & Accessories","Clothing, Shoes and Jewelry","Collectibles & Fine Art","Computers","Electronics","Garden & Outdoor","Grocery & Gourmet Food","Handmade","Health, Household & Baby Care","Home & Kitchen","Industrial & Scientific","Kindle","Luggage & Travel Gear","Movies & TV","Musical Instruments","Office Products","Pet Supplies","Sports & Outdoors","Tools & Home Improvement","Toys & Games","Video Games"]
potStatus = ['Fulfilled', 'Not Fulfilled']

fake = Faker()
fake.add_provider(internet)
fake.add_provider(misc)
fake.add_provider(lorem)
fake.add_provider(date_time)
fake.add_provider(profile)

def generateRandomData(numUsers, numProducts, numOrders):
	sellersArr = []
	emailArr = []
	# with open('db/data/Users.csv', 'w', newline='') as users, open('db/data/LoginInformation.csv', 'w', newline='') as pwd:
	# 	#Users: uid, email, pass, firstname, lastname, address, balance
	# 	uWriter = csv.writer(users)
	# 	pWriter = csv.writer(pwd)
	# 	for i in range(1, numUsers+1):
	# 		uid = i
	# 		if i%20 == 0:
	# 			print(i)
	# 		unhashed = fake.password(length=random.randint(10, 30))
	# 		password = generate_password_hash(unhashed)
	# 		prof = fake.simple_profile()
	# 		while prof['mail'] in emailArr:
	# 			prof = fake.simple_profile()
	# 		emailArr.append(prof['mail'])
	# 		name = prof['name'].split(" ")
	# 		firstName = name[0]
	# 		lastName = name[1]
	# 		addr = prof['address']
	# 		balChoices = [0, 0, 0, round(random.uniform(0, 1000), 2)]
	# 		bal = random.choice(balChoices)
	# 		pWriter.writerow([uid, prof['mail'], unhashed])
	# 		uWriter.writerow([uid, prof['mail'], password, firstName, lastName, addr, bal])

	# with open('db/data/Sellers.csv', 'w', newline='') as sellers:
	# 	sWriter = csv.writer(sellers)
	# 	for i in range(1, numUsers+1):
	# 		if random.randint(1, 4) == 1: # 25% chance of a given user also being a seller
	# 			sWriter.writerow([i])
	# 			sellersArr.append(i)

		
	with open('db/data/Products.csv', 'w', newline='') as prods:
		#Products: pid, deleted, sid, name, desc, category, pic, price, quantity
		file = open('db/data/Sellers.csv')
		csvreader = csv.reader(file)
		for row in csvreader:
			sellersArr.append(row[0])
		pWriter = csv.writer(prods)
		for i in range(1, numProducts+1):
			pid = i
			deleted = False
			if 5 == i % 200:
				deleted = True
			uid = random.choice(sellersArr)
			itemDesc = fake.sentence(nb_words=random.randint(10,20))
			category = random.choice(categories)
			catList = category.split(" ")
			if "&" in catList:
				catList.remove("&")
			objName = fake.word().capitalize() + " " + random.choice(catList)
			price = round(random.uniform(0.99, 100), 2) + random.choice([0, 0, 0, 0, 0, 100])
			quant1 = random.choice([1, 2, 3, 5, 5, 5, 5, 10, 10, 10, 10, 20, 20, 100, 100])+random.randint(1, 9)
			picture = category.split(" ")[0].lower()
			pData = [pid, deleted, uid, objName, itemDesc, category, '/static/images/' + picture + ".jpg", price, quant1]
			pWriter.writerow(pData)


			
			
		
	"""with open('db/data/OrderInformation.csv', 'w', newline='') as ordInfo:
		#OrderInformation: oid, uid, date
		oiWriter = csv.writer(ordInfo)
		for i in range(1, numOrders+1):
			uid = random.randint(1, numUsers)
			oid = i
			date = fake.date_time_this_year()
			address = fake.simple_profile()['address']
			oiWriter.writerow([oid, uid, date, address])

	with open('db/data/ItemsInOrder.csv', 'w', newline='') as itemsInOrd:
		#ItemsInOrder: oid, pid, quantity2, price, status
		iioWriter = csv.writer(itemsInOrd)
		for i in range(1, numOrders+1):
			pids = []
			oid = i
			totallyFulfilled = random.choice([True, True, True, False])
			for j in range(1, random.randint(2, 7)):
				pid = random.randint(1, numProducts)
				while pid in pids:
					pid = random.randint(1, numProducts)
				status = random.choice(potStatus)
				time_fulfilled = ''
				if totallyFulfilled:
					status = "Fulfilled"
				if status == "Fulfilled":
					time_fulfilled = fake.date_time_this_year()
				quant2 = random.choice([1, 1, 1, 1, 2, 2, 3, 4])
				pids.append(pid)
				price = round(random.uniform(0.99, 100), 2) + random.choice([0, 0, 0, 0, 0, 100])
				iioWriter.writerow([oid, pid, quant2, price, status, time_fulfilled])"""

	# with open('db/data/ProductReview.csv', 'w', newline='') as prodRev:
	# 	#ProductReview: uid, pid, rating, desc
	# 	prWriter = csv.writer(prodRev)
	# 	for i in range(1, numProducts+1):
	# 		avgRating = random.randint(1, 5)
	# 		uids = []
	# 		for j in range(1, random.randint(2, 7)):
	# 			uid = random.randint(1, numUsers)
	# 			while uid in uids:
	# 				uid = random.randint(1, numUsers)
	# 			pid = i
	# 			pRating = random.choice([1, 5, avgRating])
	# 			pDesc = fake.sentence(nb_words=random.randint(10,20))
	# 			uids.append(uid)
	# 			date = fake.date_time_this_year()
	# 			prWriter.writerow([uid, pid, pRating, pDesc, date])
			
	# with open('db/data/SellerReview.csv', 'w', newline='') as slrRev:
	# 	#SellerReview: uid (buyer), uid(seller), rating, review
	# 	srWriter = csv.writer(slrRev)
	# 	for i in sellersArr:
	# 		sid = i
	# 		avgRating = random.randint(1, 5)
	# 		uids = []
	# 		for j in range(1, random.randint(2, 7)):
	# 			uid = random.randint(1, numUsers)
	# 			while uid in uids:
	# 				uid = random.randint(1, numUsers)
	# 			sRating = random.choice([1, 5, avgRating])
	# 			sRev = fake.sentence(nb_words=random.randint(10,20))
	# 			uids.append(uid)
	# 			date = fake.date_time_this_year()
	# 			srWriter.writerow([uid, sid, sRating, sRev, date])

	# with open('db/data/Carts.csv', 'w', newline='') as carts:
	# 	#Carts: uid, pid, quantity3
	# 	ctsWriter = csv.writer(carts)
	# 	for i in range(1, numUsers+1):
	# 		uid = i
	# 		pids = []
	# 		for j in range(1, random.choice([1, 1, 2, 3, 4, 5, 6, 7])):
	# 			pid = random.randint(1, numProducts)
	# 			while pid in pids:
	# 				pid = random.randint(1, numProducts)
	# 			pWhenP = round(random.uniform(0.99, 2000))
	# 			ctsWriter.writerow([uid, pid, random.choice([1, 1, 1, 1, 2, 2, 3, 4])])

	# with open('db/data/Messages.csv', 'w', newline='') as messages:
	# 	#Carts: uid, pid, quantity3
	# 	ctsWriter = csv.writer(messages)
	# 	for i in range(1, numUsers+1):
	# 		mid = i
	# 		sender_id = random.randint(1,numUsers)
	# 		recipient_id = random.randint(1,numUsers)
	# 		while recipient_id == sender_id:
	# 			recipient_id = random.randint(1, numUsers)
	# 		subject = fake.sentence(nb_words=random.randint(2,5))
	# 		msg = fake.sentence(nb_words=random.randint(15,200))
	# 		msg_read = random.choice(['Unread', 'Read', 'Read', 'Read'])
	# 		date = fake.date_time_this_year()
	# 		ctsWriter.writerow([mid, sender_id, recipient_id, subject, msg, msg_read, date])

	# with open('db/data/SaveForLater.csv', 'w', newline='') as save:
	# 	#Carts: uid, pid, quantity3
	# 	ctsWriter = csv.writer(save)
	# 	for i in range(1, numUsers+1):
	# 		if random.choice([0,0,0,0,0,1]) == 1:
	# 			uid = i
	# 			pid = random.randint(1, numProducts)
	# 			quantity = random.choice([1,1,1,2,2,3,4])
	# 			ctsWriter.writerow([uid,pid,quantity])
	# return None

generateRandomData(10000, 10000, 20000)