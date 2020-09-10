from flask import Flask, jsonify
import pymongo
import re, string

# initiate app
app = Flask(__name__)

# connect to database
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client.restaurant_db

# define routes
@app.route("/")
def index():
    # homepage which provides query paths
    return (
        "<h1 style='text-align: center;'>Foodies DB</h1><br/>"
        "<div style='text-align: center;'>"
        "<strong>Search by Name:</strong> /api/v1.0/search/name/{restaurant name}<br/><br/>"
        "<strong>Search by City:</strong> /api/v1.0/search/city/{city name}<br/><br/>"
        "<strong>Search by Name and City:</strong> /api/v1.0/search/name_city/{restaurant name}/{city name}<br/><br/>"
        "<strong>Search by Zip Code:</strong> /api/v1.0/search/zipcode/{zip code}<br/><br/>"
        "<strong>Search by Name and Zip Code:</strong> /api/v1.0/search/name_zipcode/{restaurant name}/{zip code}<br/><br/>"
        "<strong>Search by Phone Number:</strong> /api/v1.0/search/phone/{phone number}<br/><br/>"
        "<strong>Total Record Count:</strong> /api/v1.0/search/zipcode_count<br/><br/>"
        "</div>"
    )

@app.route("/api/v1.0/search/name/<name>")    
def search_by_name(name):
    # normalize name for optimal search results
    name = name.lower()
    name = re.sub("\'(.*)", "", name)
    name = name.replace(" ","-")
    return_list = []
    # retrieve all restaurants in db
    for restaurant in db.yelp.find():
        # search all alias names for match
        if name in restaurant["alias"]:
            # remove mongodb's "_id" field (incompatable with jsonify)
            restaurant.pop("_id")
            return_list.append(restaurant)

    return jsonify(return_list)

@app.route("/api/v1.0/search/city/<city>")
def search_by_city(city):
    # normalize city name
    city = city.title()
    return_list = []
    # retrieve all restaurants in city
    for restaurant in db.yelp.find({"location.city":city}):
        # remove mongodb's "_id" field (incompatable with jsonify)
        restaurant.pop("_id")
        return_list.append(restaurant)
    
    return jsonify(return_list)

@app.route("/api/v1.0/search/name_city/<name>/<city>")    
def search_by_name_city(name, city):
    # normalize variables for optimal search results
    name = name.lower()
    name = re.sub("\'(.*)", "", name)
    name = name.replace(" ","-")
    city = city.title()
    return_list = []
    # retrieve all restaurant in city
    for restaurant in db.yelp.find({"location.city":city}):
        # search all alias names for match
        if name in restaurant["alias"]:
            # remove mongodb's "_id" field (incompatable with jsonify)
            restaurant.pop("_id")
            return_list.append(restaurant)

    return jsonify(return_list)

@app.route("/api/v1.0/search/zipcode/<zipcode>")
def search_by_zipcode(zipcode):
    return_list = []
    # retrieve all restaurants in zipcode
    for restaurant in db.yelp.find({"location.zip_code":zipcode}):
        # remove mongodb's "_id" field (incompatable with jsonify)
        restaurant.pop("_id")
        return_list.append(restaurant)
    
    return jsonify(return_list)

@app.route("/api/v1.0/search/name_zipcode/<name>/<zipcode>")    
def search_by_name_zipcode(name, zipcode):
    # normalize variables for optimal search results
    name = name.lower()
    name = re.sub("\'(.*)", "", name)
    name = name.replace(" ","-")
    return_list = []
    # retrieve all restaurant in city
    for restaurant in db.yelp.find({"location.zip_code":zipcode}):
        # search all alias names for match
        if name in restaurant["alias"]:
            # remove mongodb's "_id" field (incompatable with jsonify)
            restaurant.pop("_id")
            return_list.append(restaurant)

    return jsonify(return_list)

@app.route("/api/v1.0/search/phone/<phone>")
def search_by_phone(phone):
    # add country code to phone number (US phone numbers only)
    return_list = []
    phone = f"+1{phone}"
    # retrieve all restaurants with matching phone number
    for restaurant in db.yelp.find({"restaurant_phone":phone}):
        # remove mongodb's "_id" field (incompatable with jsonify)
        restaurant.pop("_id")
        return_list.append(restaurant)
        
    return jsonify(return_list)

@app.route("/api/v1.0/search/zipcode_count")
def zipcode_restaurant_count():
	# retrieve total count of records
    zip_code_restaurant_count =db.yelp.aggregate([{"$group": {"_id": "location.zip_code", "Total Record Count" : {"$sum": 1}}}])
    return_list = []
    for restaurant in zip_code_restaurant_count:
        # remove mongodb's "_id" field (incompatable with jsonify)
        restaurant.pop("_id")
        return_list.append(restaurant)

    return jsonify(return_list)


if __name__ == "__main__":
    app.run(debug=True)