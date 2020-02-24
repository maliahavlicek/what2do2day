# What2Do2Day Data Model
## Author
Malia Havlicek
>## Table of Contents
> - [Initial](#Initial)
> - [Mid Project](#Mid-Project)
> - [Final](#Final)
> - [Metrics](#Metrics)

### Initial
The data model for places was originally formed from google's MAPS api for places. I already had de-scoped the need to permissions and various user roles, but I did have an overly granular break down of address components:
![initial model](images/data_model/Data-Diagram-Initial.png)


### Mid-Project 
After beginning to build the place entry form, I began to see that there was no need to be so detailed with addresses. I eliminated quite a few data models and collapsed some fields to static choices that did not need a model to store them with respect to ratings and prices.
![mid-project](images/data_model/Data-Diagram.png)

### Final
Once I built the input fields and had the User Interface in front of me for all components, I saw that I didn't need to have an ages model in the database. As I added in map functionality, I updated the address data model to store the results of my google API queries in an effort to reduce API calls. I also found that it would be best to keep countries in a database as the list is long and if I ever decide to tie postal_code regex validation to a country, a database model would be much easier to maintain than a json data structure. I also refactored the enabled attribute to be share. 
![final](images/data_model/Final%20Data%20Diagram-Objects%20For%20App.png)

### Metrics
Metrics were the last data models I built. Ideally I'd track devices and screen widths so future enhancement could be catered to the largest audience, but I did not find a reliable way in python to grab such data across various operating systems for page metrics. But once more research is done, I should be able to easily add that information into both the PAGES and CLICK metric tables.
![final](images/data_model/Final%20Data%20Diagram-Metrics.png)

