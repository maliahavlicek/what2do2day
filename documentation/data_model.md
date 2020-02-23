# What2Do2Day Data Model
## Author
Malia Havlicek
>## Table of Contents
> - [Initia](#Initial)
> - [Mid Project](#Mid-Project)
> - [Final](#Final)
> - [Metrics](#Metrics)

### Initial
The data model for places was originally formed from google's MAPS api for places. I also invisioned the need to permissions and various users and a very granular break down of address components.
![initial model](images/data_model/Data-Diagram-Initial.png)


### Mid-Project 
After discarding the complexity of users and seeing that there was no need to be so granular with addresses, I eliminated quite a few data models and collapsed some fields to static choices that did not need a model to store them.
![mid-project](images/data_model/Data-Diagram.png)

### Final
Once I built the input fields and had the User Interface in front of me, I saw that I needed to have an activities model in the database. This helped facilitate the ease of custom activity icon and names on the fly. As I added in map functionality, I enlarged to the address data model to store the results of my google API queries in an effort to reduce  API calls. I also found that it would be best to keep countries in a database as the list is long and if I ever decide to tie postal_code regex validation to a country, a database model would be much easier to maintain than a json data structure. Likewise, I figured out I did not need a rating model nor an ages model as those choices were very small. 
![final](images/data_model/Final%20Data%20Diagram-Objects%20For%20App.png)

### Metrics
Metrics were the last data models I built. Ideally I'd track devices and screen widths so future enhancement could be catered to the largest audience, but I did not find a reliable way in python to grab such data across various operating systems for page metrics. But once more research is done, I should be able to easily add that information into both the PAGES and CLICK metric tables.
![final](images/data_model/Final%20Data%20Diagram-Metrics.png)

