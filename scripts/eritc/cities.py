from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import time
import pymongo


links={}
unique=True
count=-20


while unique == True:
		count += 20
		url=f'https://everyrestaurantinthecity.com/colorado-restaurants/{count}'
		print(f'This is the url: {url}')
		time.sleep(10)
		try:
			html=urlopen(url)
			time.sleep(3)
			soup=bs(html, 'html.parser')
			for rows in soup.find_all('td', width='33%'):
				for row in rows.find_all('a'):
						links[row.text]=row.attrs['href']
						
		except:
			unique = False
			print('Last Page Reached')


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://127.0.0.1:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.restaurant_db
collection = db.cities

for key, value in links.items():
	post = {'city': key,
			'url': value}
	
	collection.insert_one(post)



	

