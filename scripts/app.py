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
        "<strong>Search by Name:</strong> /api/v1.0/search/name/{restaurant_name}<br/><br/>"
        "<strong>Search by City:</strong> /api/v1.0/search/city/{city_name}<br/><br/>"
        "<strong>Search by Name and City:</strong> /api/v1.0/search/name_city/{restaurant_name}/{city_name}<br/><br/>"
        "<strong>Search by Zip Code:</strong> /api/v1.0/search/zipcode/{zip_code}<br/><br/>"
        "<strong>Search by Phone Number:</strong> /api/v1.0/search/phone/{phone_number}<br/><br/>"
        "</div>"
    )

@app.route("/api/v1.0/search/name/<name>")    
def search_by_name(name):
    # normalize name for optimal search results
    name = name.lower()
    name = re.sub("\'(.*)", "", name)
    name = name.replace(" ","-")
    # search all alias names for match
    return_list = []
    # retrieve all records in db
    for restaurant in db.yelp.find():
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
    # search all alias names for match
    return_list = []
    # retrieve all records in db
    for restaurant in db.yelp.find({"location.city":city}):
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

@app.route("/api/v1.0/search/phone/<phone>")
def search_by_phone(phone):
    # add country code to phone number (US phone numbers only)
    return_list = []
    phone = f"+1{phone}"
    # retrieve all restaurants with the same phone number
    for restaurant in db.yelp.find({"restaurant_phone":phone}):
        # remove mongodb's "_id" field (incompatable with jsonify)
        restaurant.pop("_id")
        return_list.append(restaurant)
        
    return jsonify(return_list)


if __name__ == "__main__":
    app.run(debug=True)