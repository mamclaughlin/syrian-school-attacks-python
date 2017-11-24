######################################
#DEPENDENCIES
######################################
from splinter import Browser
from bs4 import BeautifulSoup
import time
import requests
import pymongo
import re
import Keys

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)
#Syrian schools info url
url = 'http://sn4hr.org/page/1/?s=school'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
pageMax = int(soup.find('a', class_="last").text) + 1

######################################
#MONGO SETUP
######################################
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://' + Keys.user + ':' + Keys.password + '@ds121456.mlab.com:21456/heroku_63785bfl'
#'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.syria_db
collection = db.items

######################################
#URL COLLECTION STEP
######################################
#urls from the news articles
urls = []

#loop through all the pages on the site 
#and grab urls from each headline and push to array (url)
#pageMax
for x in range(1,pageMax):
	try:
		######################################
		#SPLINTER SETUP
		######################################
		#Open chrome browser, don't open webpage --> (headless = true)			
		executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
		browser = Browser('chrome', **executable_path, headless=True)

		#URL to syrian site and request to get that url
		url = 'http://sn4hr.org/page/' + str(x) + '/?s=school'
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')

		#find anchor tags of only those who have 'h3' as a parent, then append to urls array
		for ana in soup.findAll('a'):
			if ana.parent.name == 'h3':
				urls.append(ana["href"])
				# print(x)
				# print(ana["href"])

	except Exception as e:
		print(e)

	print(x)
	#sleep to prevent getting blocked
	time.sleep(1)



######################################
#TEXT COLLECTION STEP
######################################
#collect urls, then go into them and get info
text = []

#iterate through urls array we created in first step, then grab the designated text and push to array
for getUrl in urls:
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=True)

	# url = getUrl
	response = requests.get(getUrl)
	soup = BeautifulSoup(response.text, 'html.parser')	

	try:
		#get url from array of urls
		browser.visit(getUrl)
		full_text = soup.body.find('h5').text.lower()

		if 'school' in full_text or 'School' in full_text:
		#find summary from each page
			
			#find who fired
			who_fired = full_text[7:35].replace('fire', '').lower()

			# date
			date = full_text[-20:-2]
			#strips off everything before the date so output is i.e: January 20, 2017 
			new_date = re.sub('^(.*)(?=(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?))', '', date)

			#school
			pattern = re.compile(r" on | near ")
			school = (pattern.split(full_text)[1]).split("school")[0] + "school"

			#level of damage
			# damage = 

			#append full text to array
			text.append(full_text)

			#===================

			attackers = ['suspected Russian warplanes', 'regime warplanes', 'armed opposition', 'government warplanes',
			'government warplanes (allies)','government helicopters','government forces','ISIS artillery','Syrian-Russian alliance warplanes',
			'armed opposition factions','International Coalition warplanes', 'local made rocket shells', 'unknown-source']

			count = 0

			#iterate through list of possible attackers
			for attacker in attackers:

				if attacker in full_text:
					count += 1
					if count > 0:

						# print('-----------')
						# print('school: ')
						# print(school)
						# print('attacker: ' + attacker)
						# print('date: ' + new_date)
						# print('full text: ' + full_text)
						# print('url: ' + getUrl)

						# Dictionary to be inserted as a MongoDB document
						post = {
						    'who_fired': attacker,
						    'school': school,
						    'date': new_date,
						    'link': getUrl,
						    'full_text': full_text,
						}	
						collection.insert_one(post)

					else:
						who_fired = item[7:35].replace('fire', '')

						# print('-----------')
						# print('school: ')
						# print(school)
						# print('attacker: ' + who_fired)
						# print('date: ' + new_date)
						# print('-----------')
						# print('full text: ' + full_text)
						# print('url: ' + getUrl)

						# Dictionary to be inserted as a MongoDB document
						post = {
						    'who_fired': who_fired,
						    'school': school,
						    'date': new_date,
						    'link': getUrl,
						    'full_text': full_text,
						}
						collection.insert_one(post)

	except Exception as e:
		print(e)

	time.sleep(1)

articles = db.items.find()

for article in articles:
	print(article)





