# foodies_api

Project Description:

The project focuses on providing restaurant data to interested parties through an API. The project objectives are to create an API where interested parties can access specific Colorado restaurant data for purposes of analysis based on multiple datapoints or a single datapoint.  The database we are using MongoDB.

Data Extraction:

Our data is extracted from two main resources.
The first source of data was acquired by scraping www.everyrestaurantinthecity.com  (eritc). The website has no API portal so, the only way to gather the data available here is by scraping the web pages.  Firstly, we read the “Terms & Conditions” for this website.  Nowhere in this document did it prohibit scraping of the website.
So, we proceeded to write python scripts to scrape the data from the pages.
The second source of our data comes from Yelp API.  This service provides a key to users who request one for purposes of creating an application/service that at least in part utilizes data we collect from the Yelp API.  Once we loosely define our project, we are granted a data access key that enables us to make up to 5000 queries in any given 24-hour period.
In order to scrape eritc we began development of code on two fronts. The first scraping process was to utilize the fact that with each page loaded of homogenous data the page address tacked on a number that is linearly incremented.  So, for example to scrape the page addresses for each city in Colorado we went to the city index pages and for each page the web address is incremented by 20.  So, eritc.com/city-state/20 goes to eritc.com/city-state/40.
This method worked fine for gathering the city restaurants web page data but, ended up not being a reasonable method to gather the specific restaurant data.  For purposes of gathering the specific/atomic restaurant data we utilized ‘splinter’ a tool which will ‘click’ active anchor links navigating to each progressive page and gathering needed data.  Once this was done, we reviewed this data confirming we are able to leverage this data to gather more restaurant atomic data from Yelp API.
The Yelp API provided us an opportunity to access more information for our project than was available from eritc.  Additional information we gathered is restaurant: category, photo links, 
geographic coordinates, price range, hours of operation, review counts, a small selection of reviews, and the Yelp web page address.  We added this information to each restaurant record.
A script was created that returned atomic restaurant information gathered on eritc for each restaurant.  This base data was used to query Yelp API to retrieve the additional information listed above. By leveraging data from one resource we are able to more efficiently add additional useful information to our dataset for use by interested parties accessing our API.

Data Transformation:

In our dataset gathered from eritc we observed that there were repeated restaurants.  In order to clean the data of repeated records we added code to our Yelp API query script to check for duplicates in the data that Yelp returned to our queries.  This duplicate data was skipped over and not added to the container of data we were gathering to place in our new collection/table of data we were creating with the Yelp data.  So, in this way we are able to gather more data and efficiently clean our data of duplicates as parts of the same larger process.  Further, if a restaurant that was in our original eritc dataset was not found on Yelp we dropped those records.  We based this decision on the presupposition that: The Yelp data is comparatively more reliable than eritc data due to Yelp’s extensive use by consumers and the extensive resources that Yelp has to improve/maintain their dataset.  And thusly, if the restaurant we are searching for with eritc data is not in the Yelp dataset we concluded the specific restaurant data, we had from eritc was either inaccurate or the restaurant is no longer in business.

Data Loading:

Since we used MongoDB our data set is “flat”.  That is to say, it is document based.  We choose this data management infrastructure because the data we are collecting is not complex.  The data is only of the type “restaurant”.  We do not have other data that would be considered heterogenous to the restaurant data.  For example, if we were to at some point want to provide data regarding the city the restaurant is in or a dataset of annual events in the area where the restaurant is located.  The incorporation of this additional information would lead us to consider a relational data management system as possibly being a more appropriate management system to move our data.   We would only do this for the organization and efficient management of our data.  As our resource of data grows and expands into a multitude of category types.  Though we will likely weigh all of our data management options as our project becomes larger and more complex.  This being said, we could almost certainly, successfully, stay with the document data model and be just fine.  Other reasons we chose the document model for our data is the ease of getting up and running compared to a relational model.  Also, accessing data is overall faster with our document model.  Another benefit is we need less code to access and manage our dataset with the document model.
        ## eritc base data
![Alt eritc_base_data](/images/eritc_base_data.png)

API:

Our API provides multiple access points to retrieve data.  We have an index page that provide a list of query paths to access our restaurant data.  Individual records can be returned via a restaurant by name query string.  A query string is provided to query restaurant by city. This is useful in the case where a particular restaurant has locations in multiple cities.  Our API further provides a query path for accessing a list of restaurants by zip code.  Additionally, our API provides a query path for finding a specific restaurant by name and zip code.  This is an alternate method to the query by city and restaurant name.  A query string is provided to access restaurant data by restaurant phone number.  Lastly, we provide a query string to access a count of restaurants by zip code.  This data is readily usable to create a bar chart illustrating which zip codes have more or fewer restaurants.  A future further extension of this concept will be to provide the restaurant count by city.

Final Thought:

This project accomplishes all of the resource provisioning and functionality we envisioned at the beginning of our project.  We plan on continuing to add functionality to this API providing additionally relevant information about events and city statistics as mentioned above. Perhaps in the future we will add an HTML graphical user interface for non-technically inclined interested parties.



