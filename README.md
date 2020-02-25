# What2Do2Day
URL: http://what2do2day.herokuapp.com/

## Author
Malia Havlicek
## Project Overview
This website provides people a way to find free events in their community as a means to solve the question of "What are we gonna do today?" without breaking the bank or needing to travel far from home. Along with finding inexpensive options of what to do today, the site allows users to flag that they are planning on attending an event so other members know they will not be the only one going to a function. The target user for this app is 12 -18 years of age, children that are independent without individual transportation or lots of spare change. The site can easily be scaled up to include more predefined age ranges if the market determines there is a need.

Users can also view a list of all the places in the community that have ever hosted an event and read reviews about them. Parents, children, members of the community can add reviews about places to share their experiences and rate organizations. Places and Events can be created, read, and soft deleted from the site, while reviews can only be created and read. Rather than forcing users to place activities into a predefined list, users freely associate places and events with  activities during creation based on a name and icon selection. Small businesses, social groups, and communities would ideally be in charge of their organizations's data and events but in this beta phase, user authentication, roles and permissions are not implemented, hence soft deletes and no updating of reviews.

Site owners could enable affiliate linking from any organization associated with the site that results in a sale from the place's own website.  By adding a Google Click Identifier (GCLID) to a place's url when leaving What2Do2Day's site, offline conversions could be tracked and negotiated to a monetary value for the site owners. Site admins could also gather data based on search activity as well as Places and Events with heavy interaction and sell ads on this site to help earn money by targeting audiences of similar interests. (Note how the Places's page has natural side bars in desktop when users are looking at events and reviews, on mobile devices ad space could be inserted below filtering options and above the footer too.)

The name and concept of this site is loosely based on the key phrase, "I know what we're gonna do today!" from the cartoon series [Phineas and Ferb](https://en.wikipedia.org/wiki/Phineas_and_Ferb).
 
## <summary>Table of Contents</summary>
> - [UX](#UX)
>   - [Strategy](#Strategy)
>   - [Scope](#Scope)
>   - [Structure](#Structure)
>   - [Skeleton](#skeleton)
>   - [Surface](#surface)
>     - [Color Choice](#color-choice)
>     - [Typography](#typography)
>     - [Image Choice](#image-choice)
>     - [Design Elements](#design-elements)
>     - [Animations & Transitions](#animations--transitions)
>   - [User Stories](#user-stories)
>     - [For Community Members](#for-kids-looking-for-something-free-to-do-today-in-their-neighborhood)
>     - [For Places and Organizations](#for-places-and-organizations-involved-in-building-the-community)
>     - [For Site Owners](#for-site-owners-hosting-a-website-to-store-community-information)
>   - [Features](#features)
>     - [Implemented](#implemented-features)
>       - [Structural](#structural)
>       - [Common Elements](#common-elements)
>       - [Forms](#forms)
>       - [Data Operations](#data-operations)
>       - [API Integration](#api-integration)
>       - [Metrics](#metrics)
>     - [Future](#features-left-to-implement)
>       - [User Roles & Permissions](#user-roles--permissions)
>       - [Place Administrator Dashboard](#place-administrator-dashboard)
>       - [External User Adult Dashboard](#external-user-adult-dashboard)
>       - [External User Minor Dashboard](#external-user-minor-dashboard)
>       - [Content Admin Dashboard](#content-admin-dashboard)
>       - [Site Admin Dashboard](#site-admin-dashboard)
>       - [API Integration](#api-integrations)
> - [Project Tracking](#project-tracking)
> - [Technologies Used](#technologies-used)
>     - [Programming languages](#programming-languages)
>     - [Framework & Extensions](#framework--extensions)
>     - [Fonts](#fonts)
>     - [Tools](#tools)
>     - [APIs](#apis)
> - [Testing](#testing)
>   - [validation](#validation-testing)
>   - [unit](#unit-testing)
>   - [cross browser](#cross-browser-cross-device-verification)
>   - [XSS & CSFR](#cross-site-scripting-and-forgery)
>   - [accessibility](#accessibility-testing)
>   - [regression](#regression-testing)
>   - [automated](#automated-testing)
> - [Deployment](#deployment)
>   - [Requirements](#requires)
>   - [Local](#running-locally)
>   - [Heroku](#heroku)
> - [Credits](#credits)
>   - [content](#content)
>   - [media](#media)
>   - [Acknowledgements](#acknowledgements)


## UX
### Strategy
Before launching any website, business partners want to know how they can earn money and if there is a need or demand for the project. Defining business goals of a project from the standpoint of an external user as well as site owners helps you evaluate possible return on investment.

Upon reading the suggested projects for the Data Centric Milestone Project, I came up with
<details>
<summary>2 Ideas: </summary>

1.Texting Translator:
> External Goals
>  - Lookup definitions so you know what LOL and MILF means before determining if you need to have a serious talk with your children
>  - Find out what your savvy friend means rather than embarrassing yourself by asking your clueless parents
>  - Correct poor definitions by providing a new one and down voting the older definitions so people are better informed
>
> Site Owner's Goals
>  - Publish T-shirts, & stickers mugs for benign but up to date trends
>
> Features
>   - Create an app that allows users to upload Texting Terms, definitions 
>   - Allow users to Up and Down voting if Definition is Accurate or not.
>   - Create back end code to manage:
>     - Terms
>     - Definitions
>     - Votes
>   - Search, allow users to search terms for a texting phrase they are unfamiliar with 
>   - Metrics about what words were search for the most so owner can Stock Online store accordingly

2.What2Do2Day:
> External Goals
>  - As a parent, find something safe for your kids to do near home that doesn't break the bank
>  - As a kid, find something that's interests me to do with my friends when mom and dad take away my electronics
>  - As a place or organization, bring attention to your business or group by being involved in the community
> 
> Site Owner's Goal
>  - Earn money from affiliate links to businesses that post their places on site when links lead to online sales
>  - Track most popular activities on site to score some money from ads
> 
> Features
>  - Create an app that allows users to upload details about places to do things with kids. Main objects are Places and Events tied to them
>  - Allow users to write reviews about places and rate them
>  - Allow users to follow a place so they know new events posted by that business
>  - Allow users to join an event so other members know how many people might show up 
>  - Create back end code to manage:
>    - Reviews
>    - Places
>    - Events
>  - Search, allow searching by activity as means to filter results
>  - Metrics - track follows to business and joins to business as well as visitors to site.

Out of these two concepts, I weighed the pros and cons of each:

__Texting Translator__ 
            
|             Pros               |                        Cons                        |
|--------------------------------|----------------------------------------------------|
| MVP could go live              | Rather Simple                                      |
| Moderate  UX                   | No API integration                                 |
| Scalable to world market       |                                                    |
| Ad & product earnings moderate |                                                    |

__What2Do2Day__

|             Pros               |                        Cons                        |
|--------------------------------|----------------------------------------------------|
| Integration with Google Maps   | Very complex                                       |
| Challenging UX                 | MVP not production worthy, anyone can make updates |
| Scalable to world market       | MVP not production worthy, (kid safety first)      |
| Earnings from Ads is high      |                                                    |
| Social Need is high            |                                                    |

 What2Do2Day has the ability to reach a broader scope of users and could potentially take off like the Nextdoor app.  What2Do2Day is more intriguing and likely to keep users coming back to the site. As a developer, the What2Do2Day app will provide greater value in the long term towards my coding skills due to it's complexity.
</details>

***
### Scope
The concept of What2Do2Day can get extremely intertwined when looking at permissions and roles. I decided that a beta version that eliminates authentication, permissions and roles can still provide a clean and efficient minimal viable product (MVP).  Thus user profiles and management of users will not be in the first deliverable. 

Restricting results based on user's location increments of 1, 5, and 10 miles would be ideal for a long term solution but it is not necessary for the MVP. Since I do not have experience with Google Maps's Nearby API, this bit of scope will be deferred until a polished core product is financed. Also not enough data will be loaded to make searching and geolocation viable initially.

Creating, reading and updating deleting functionality will only be accessible from menu options. This will allow the MVP to be built to serve the majority of long term users and keep the UX cleaner without an overwhelming amount of buttons. Admin proximity/ease of use functionality can be added after such roles are clearly defined. 

Consolidating Delete functionality into a share property reduces pages to develop. It also reduces the number of items in the menus and makes overall navigation easier while protecting the data's integrity by avoiding jumps in auto generated id's.

Business logic to track search requests, and the events and places that users interact with will be collected.  This will aide in negotiating affiliate link deals and ads will be included but graphical visualization will not be included in the MVP, only a list of the data collected. Likewise we need to know how many users are coming to the site and what percentage of them interact or do not interact with our buttons so we will attempt to track unique visits to our site and core functionality clicking attributes.

### Structure
In order to have a better idea of the tables, forms and the relationships between them I looked at google Maps' Places API to help determine what fields my place object should have. Knowing the data fields I may want to have and those that were extraneous, helped me devise a rough Entity Relationship Diagram(ERD). Like all projects, the data model morphed a few times. [See progression of data models.](documentation/data_model.md)

![final](documentation/images/data_model/Final%20Data%20Diagram-Objects%20For%20App.png)

### Skeleton
Having the data structure in hand, I knew what data fields I had at hand to present users managing the PLACES, EVENTS and REVIEW objects. I'm not a great artist but I find it easier start hand drawn markups before diving into a wireframing tool. I drafted out the home screen as well as the places list to kick start decisions concerning what data had higher priority.
[view hand drawn mockups](documentation/handdrawn.md)

Once I had the Places list drawn out, I invested several hours to mockup and fine tune the user experience using Basalmiq.
[view balsamiq deck](documentation/balsamiq.md)

Taking the time to do more formal mockups exposed an issue with the crowding of edit buttons and delete buttons. I decided that delete is really an update function since I am using the enabled attribute to hide or show items on the Places and Events pages.  The more formal mockups also allowed me to try several different layouts of the data for the main list pages. The mockkups include layers for searching and in site adding of reviews. Search non-happy paths were also mocked up. 

#### Content Considerations
Many UX decisions made had the target audience of 12 - 18 years in mind. The lack of maps on some pages was a conscious choice as the majority of users will be very familiar with the 1-5 mile radius around their home base. I wanted information spaced out with iconic/graphic identification so the users would know readily what interest the the most with limited reading required. 

### Surface:
Below are the decisions and internal dialogs I had to help draw out what the end product will look like.

#### Color Choice
I have never taken a course in color theory and have been told my choices of red are more orange than red so picking colors is a bit of a touchy area for me and I'd much rather have a professional UX designer help me out.  Feel free to read about this [project's color journey](documentation/color_choices.md) if you want to hear more about my struggle.  In short, my final color choices are:
![Final Pallet](documentation/images/colors/final_colors.png)

#### Typography
The target age group for this site is those that are young, bored at home whose parents desperately wish their kids would be outside interacting face to face with friends preferably doing something active.

To keep the site light and fun, I really wanted a cartoon feel to my headers that wouldn't have issues between uppercase i's and lower case L's. After some research I ended up choosing **Patrick Hand SC**:
>[![Patrick Hand SC](documentation/images/fonts/Patrick%20Hand%20SC.png "Patrick Hand SC Font")](https://fonts.google.com/specimen/Patrick+Hand+SC)

For my main content, I wanted a curvy flow to the font, but one that was easy to read without any i's and L's issues. I tested out a few fonts and decided on **Raleway**:
>[![Raleway](documentation/images/fonts/Raleway.png "Raleway Font")](https://fonts.google.com/specimen/Raleway)

Feel free to read about my [font choices](documentation/font_choices.md) if you want to know more about my decision process. 

#### Image Choice
This site's target audience is 12-18 years in age and they have a higher demand for imagery than older user groups do so I placed engaging imagery across the site:

##### Home Page 
To perpetuate the theme of Phineas and Ferb throughout the site, the cartoon's beginning image where Phineas and Ferb are in their back yard looking bored, chatting about what to do today is on the home page:

<img src="what2do2day/static/assets/images/were_gonna_build_a_rollercoaster_sm.jpg" width="300" height="auto" alt="phineas and ferb in backyard" />

##### Activity Icons
I wanted easily recognizable activities that users could quickly associate to events and places. I also wanted to give users a bit of self expression when creating events and places, so rather than allowing them to randomly load garish or naughty symbols, I decided to provide a broad set of icons to passively create activities from. I downloaded icons from [flaticon](https://www.flaticon.com/packs/outdoor-activities-32)
By having bold colorful icons, I am hoping to carry forward a cheerful and engaging website. Here are some example activity icons:

<img src="what2do2day/static/assets/images/icons/002-football-field.svg" width="50" height ="50" alt="football field icon"/> <img src="what2do2day/static/assets/images/icons/021-fishing.svg" width="50" height ="50" alt="fishing icon"/>  <img src="what2do2day/static/assets/images/icons/037-road-sign.svg" width="50" height ="50" alt="trail directions icon"/>

##### Input Icons
The site looked incredibly dull with wide full width entry fields, so I went back and broke it down into multiple columns and added slight splashes of color with icons relating to the input fields utilizing the primary site color and font awesome:  

<img src="documentation/images/form_fields.png" width="100%" height="auto" alt="form field image"/>

##### Header Image
The rest of the application's pages were not exciting compared to the home page, so I added in Perry the Platypus to my header with grass as seen in Phineas and Ferb's backyard. Perry's a character in Phineas and Ferb that goes from a boring pet to a super secret agent saver of the universe. By placing Perry at the top of every page except the home page, I am hoping to start the user off with a bit of fun before they start searching for something to do. 

<img src="what2do2day/static/assets/images/perry_the_platypus.png" width="50" height="auto" alt="perry the platypus" />

##### Modals and Errors
I wanted users to know through imagery that they had success or errors so I trolled the internet until I found a few Phineas and Ferb related images that would work.

 Phineas and Ferb giving each other a high five shows up on success layers: 
 
 <img src="/what2do2day/static/assets/images/success.png" width="100" height="auto" alt="success cheer image" />

Dr. Heinz Doofenshmirtz looking dumbfounded makes an appearance on user based failure layers: 

<img src="what2do2day/static/assets/images/oops.png" width="100" height="auto" alt="opps error image" />

Ferb wielding tools is on the application's catch all error page:  

<img src="/what2do2day/static/assets/images/fixit.png" width="100" height="auto" alt="fixit image" />

##### Loading Giff
I also added a loading gif for the maps in the event the API calls are a tad slow or if there are errors with google's API/configuration: 

<img src="what2do2day/static/assets/images/giphy_load.gif" width="100" height="auto" alt="opps error image" />


#### Design Elements
The formal wire-frame process identified the need for the following User Interface Components:

|               	|              	|                 	|
|---------------	|--------------	|-----------------	|
| top menu      	| sidebar menu 	| rating selector 	|
| modals/layers 	| accordions   	| textarea input  	|
| containers    	| pagination   	| icon selector   	|
| forms         	| maps         	| select choice   	|
| check boxes   	| buttons      	| date picker     	|
| switches      	| text input   	| drop downs      	|
 
 I did not want to invent all of the above, so I read [best css frameworks](https://www.creativebloq.com/features/best-css-frameworks) to make an informed decision on what framework to use. Foundation, Picnic, and Bulma made my short list as they appeared light weight and were frameworks I have not yet explored and I do want to get the most out of this course by picking up new technologies. After reading up a bit, I decided that [Bulma](https://bulma.io/) was the best fit for what I hoped to include in this project.
 
 I did end up modifying a few things from Bulma as there are errors with their calendar date picker and the default multi select was very ugly in appearance. I felt that customizing activity icon selections to display images greatly increased the user's willingness to interact with the app. 

#### Animations & Transitions
I trolled [codrops](https://tympanus.net/codrops/) to look for some inspiration.  The following sites provided ideas that greatly altered my original wire-frames:
 - [expanding search option](https://tympanus.net/Tutorials/ExpandingSearchBar/) 
 - [grid icon expansion](https://tympanus.net/Tutorials/ThumbnailGridExpandingPreview/)
 - [expanding overlay](https://tympanus.net/Tutorials/ExpandingOverlayEffect/)
 - [fullscreen overly](https://tympanus.net/Development/FullscreenGridPortfolioTemplate/)

By seeing live examples, it dawned on me that I could and should have a small icon or minimal data in my lists instead of cramming all the information on the screen. I went back to my designs, reduced the amount of data seen on the events and places lists pages as I know my target age group really relates to icons and gets glassy eyed if bogged down with too much text. The buttons to join an event expands out to a nearly full screen detail layer and presents all the data needed with a friendly animation.

I was also told by a test subject (son number 4) that the lists were boring. So I added some animation to slide rows in from the left and right sides of the screen and added some color to keep it a bit more upbeat that a mainly white page.

For the Review Input, the stars have a wiggle animation on desktop as the user hovers over them and a shine to the selection if you rate something a 5 star. A one star is dull to reflect the glum outlook the reviewer has.

### User Stories:
This website serves 3 sets of users, thus the stories are broken down into 3 categories:

#### For kids looking for something free to do today in their neighborhood:
  - As a user, I'd like a list of events happening.
  - As a user, I want to filter events by age and activity so I can find something to do that matches my interests.
  - As a user, I want to sort events by a date range so I can find something to do in the future easily.
  - As a user, I want to join an event so I can be reminded when it happens.
  - As a user, I want to follow a place that hosts events so I can know when a new event is added immediately.
  - As a user, I want to read reviews about places that host events, so I know what to expect.
  - As a user, I want to write a review about a place so I can share my opinion.
  - As a user, I want to remove my review about a place so I can have a low profile online.
  - As a user, if I don't enter the form data correctly, I want to know how to fix it.

#### For places and organizations involved in building the community
  - As a user, I want to list my place so the community knows about it.
  - As a user, I want to have honest reviews about my place to build trust with the community.
  - As a user, I want to remove reviews about my place so that inappropriate comments are not associated with my place.
  - As a user, I want people to follow my place so they can know about events, and so I can compare my place to other places that host similar activities.
  - As a user, I want to add events to my place so the community knows about them.
  - As a user, I want people to join my events, so I can communicate with them if details change and plan for the right number of attendees.
  - As a user, I want to disable my events if the weather doesn't cooperate.
  - As a user, I want to disable my place if I decide to retire, go on vacation, or sell my place.
  - As a user, I want to know if I make any input errors easily so I can successfully update my form.

#### For site owners hosting a website to store community information
  - As a site owner, I want a Home page that communicates the purpose of the website.
  - As a site owner, I want the ability to track search criteria to better target ad spacing on my site.
  - As a site owner, I want the ability to track places users follow to negotiate offline conversion money from those places.
  - As a site owner, I want the ability to track events users join to negotiate offline conversion money and to better target ads.
  - As a site owner, I want the ability to track reviews uses write to better gauge community engagement.
  - As a site owner, I want the ability to track user's emails for research purposes in beta, potential marketing in the future.
  - As a site owner, I don't want hackers to mess with my data base, so I don't loose all the information my users have contributed.

## Features
To streamline the development process without the complexity of user roles and permissions, it was decided that the MVP consists of a beta product as a proof of concept for a small market. The beta features are those listed in the Implemented Features. If the project is taken to it's full potential, the Features Left to Implement would be tackled.

### Implemented Features
#### Structural
1. Navbar - the navbar stays collapsed on medium and small devices. The navbar contains brand logo and links to associated sections i.e. Home, Events, Places, Contribute Update. Bulma's navbar implementation was used.
1. Footer - contains disclaimer, copyrights information, links to github repository and developer's resume
#### Common Elements
1. Speech Bubble - used on home page to inform users what the site is about
1. Icon buttons - used to indicate adding events, adding places, adding reviews, following places, joining events
1. Switches - sharing and disabling events, places and reviews. The switch acts as a soft delete of items from main lists and allows users to turn them back to being shared.
1. Date Pickers - setting up time frames of events and filtering of the events list.
1. Rating Selector - star icon based radio button to record user ratings
1. Overlays - way to disable main page while getting user input for filtering results, joining an event, adding a review
1. Checkboxes - user friendly way to hide/show  sections on update and add forms such as the place address , place event, place review, event address.
1. Icon Selector - single choice, allow users to customize a place or event's activity by name and icon, 
1. Icon Selector - multiple choice, allows users to select more than one activity when searching for events.
1. Age Selector - allow a multiple select field for ages, in adding/updating events.
1. Accordion - collapse places' reviews and events, on the places list page, expands on click, expand/collapse filters on event list page.
#### Forms
1. Add Place - validation for required fields and proper data, unique Name check, also includes conditional validation of sub forms such as address, events and reviews.
1. Update Place - validation for required fields and proper data, uniqueness check
1. Add Event - validation for required fields and proper data, unique Name and Date check
1. Update Event - validation for required fields and proper data, uniqueness check
1. Count Me In - validation for unique email in list of attendees, check for max attendees limit
1. Filter Events - allow user to filter events by activities, date range and age, checks for validity of age input
1. Add Review - validation for required fields where author email can be conditionally required depending if added from place or add review button/add review navigation.

#### Database Operations
1. Aggregated Review - from all reviews of a given place, present an average rating for a place
1. Count of event joiners - When a unique email is entered, add them to the joiner list
1. filter results for events based on updating vs reading (share field both on place and event), 
1. Create list of activities for filtering based on updating vs reading (share field both on place and event)
1. check for unique emails before adding a new user
1. check for unique place name before adding a new place or updating an existing place
1. check for unique event name /date and place combo before adding or updating an existing place
1. check for a unique user/place id and date within a week before adding a new review to a place
1. check for unique user before joining an event
1. check for max attendees not exceeded before joining an event
#### API Integration
1. Email JS - when an event is added to a place, email details to followers
1. Google Calendar - when a user joins an event, send calendar invite, when event is updated, email joiner list
1. Google Maps - show map of event location, show map of place location
#### Metrics
1. track place follows by activity type and rating - bar chart for activity type, pie chart for rating
1. track event joins by activity type and age - bar chart for activity type, pie chart for age
1. track event searches by activity and age inputs - bar chart for activity type, pie chart for age
1. track place searches by activity and review - bar chart for activity type, pie chart for rating
1. count places in db by activity type - bar chart
1. count events in system by activity type - bar chart
1. count events page hits
1. count places page hits
1. count number of home page hits
1. get numbers for joining event funnel: events page hits, join event click, send invite success, send invite user error, send invite exceed attendance error
 
### Features Left to Implement
I overestimated my abilities when originally scoping this project. I didn't account for uncovering some core issues with Bulma's [datepicker functionality](https://github.com/Wikiki/bulma-calendar/issues/163#issuecomment-584172621), nor did I anticipate as much trouble understanding the routing and parameter passing in flask.  I also spent too much time trying to figure out how to break out the controller, filtering, and utility functions from my run.py. Since this project required a greater learning curve than anticipated, some functionality had to be deferred in order to allow me to learn how to automate testing and to provide attention to cross browser/cross device validation.  
#### Features Deferred from original plan
1. Follow a place - I have used Email JS in a past project so I would not gain any skills taking this functionality on and I the UX being similar to the delivered Join Event feature I don't believe I'm loosing out on a learning opportunity by eliminating this functionality.
1. Filter Places - I tackled more complex filtering logic in the filter events layer and saw this list not getting nearly as long as the events list could be.
1. Pagination - By including a count of events or places found, the user has an idea of how many results they are seeing. Pagination isn't nearly as useful on smaller devices as the buttons are cumbersome for fingers and users are accustomed to scrolling down vs paging through results, thus pagination was differed
1. Update Review - updating and sharing reviews are tightly tied to various user roles. Since user roles were originally out of scope, it made sense to differ this functionality, especially since updating and soft delete powers have been examplified in update events and update places.

#### User Roles & Permissions
In the long term once this concept proves viable, authentication would be enabled and five sets of roles would accessing the site: 

1. <strong>Place Administrators</strong> -  users who have permissions to manage the Place, Events and Activities.
1. <strong>External Users Adults</strong> - users who have permissions to grant minor external users  access to the site. Adult users would also have permissions to manage their profile and create, edit and delete their own reviews.
1. <strong>External Users Minors</strong> - users who must be granted permissions to the site by Adult External Users. Minor users can manage their profile with limited features to help ensure their safety (no images or location settings if and when those features are added to the site). Minor users can also create, edit and delete their own reviews.
1. <strong>Content Admins</strong> -  users who approve reviews for inappropriate content and bot induced batch reviews. Content admins would also be in charge of setting up ad campaigns.
1. <strong>Site Administrators</strong> - users who have permissions to create, update and delete all the data hosted on the site (Users, Places, Events, Reviews)
#### Place Administrator Dashboard
1. Limit number of attendees on events
1. Allow cloning of events
1. Allow set up of repeating events
1. Allow emailing to event joiners
1. Allow emailing to followers
1. Approve/Disapprove reviews
1. password management
1. place profile management
#### External User Adult Dashboard
1. Allow user to upload image to share along with review
1. Allow user to set proximity radius to parse down results to  1, 2, 5, 10 mi radius
1. Allow user to share location with other members
1. Allow user to manage minors reviews/places/events/profile
1. Allow user to opt into/out of minor's following and joining behavior
1. Allow user to see and manage all reviews they've made
1. Allow user to see and manage all places they have followed
1. Allow user to see and manage all events they have joined
1. password management
1. user profile management
#### External User Minor Dashboard
1. Allow user to chose avatar to share along with review/follow/join
1. Allow user to set proximity radius to parse down results to  1, 2, 5, 10 mi radius
1. Submit reviews/place following /event joining to supervising adult
1. Allow user to see and manage all reviews they've made
1. Allow user to see and manage all places they have followed
1. Allow user to see and manage all events they have joined
#### Content Admin Dashboard
1. Manage ad placement & campaigns
1. Follow up on disapproved reviews
1. Keep up with naughty word list identification
1. Manage abuse reports
#### Site Admin Dashboard
1. Pull metrics & manage dashboard graphics
1. Manage users & permissions/role groups
1. Password reset 
#### More Sophisticated Attendance Tracking ###
1. Allow users to enter how many in their group are attending an event min 1, max dynamic to max attendees allows - those already attending
1. Aggregate attendance count based on each attendee count instead of 1 to 1 ratio currently implemented
1. Real-Time attendance count - add backend wait time loops and javascript to show attendance adjustments made by other users instead of on checking attendance limit on submit only
1. Utilize a calendar API such as Google Calendars.
#### API Integrations
1. GoogleAds - ad placement, offline conversions, automatic bidding
1. GoogleMaps Sitepoint - get directions from current location
1. GoogleMaps Geolocation - share location with other members, narrow results of events and places by proximity/nearby functionality or postal code/address entry.
1. GoogleCalendar - manage events and email notifications instead of STMP emails.
#### Switch to Relational Database
1. mongo DB is not the correct data base, it was chosen because it has a free tier, but the aggregation to force joins is awkward and inefficient. As the dataset grows this will cripple the application's efficiency.
### Project Tracking
The scope of this project was larger than a typical milestone effort and I quickly felt overwhelmed when learning new skills such as Bulma, mongodb aggregated queries, Flask Filters, Flask Macros, Flask WTF Forms, Validators, Flask blueprints and routes. 
To ensure I kept on task and could feel a sense of accomplishment while taking the countless baby steps towards completion, I devised a [project tacking sheet](https://docs.google.com/spreadsheets/d/1Lnvt9zLgJj0oQFdpOIAs1V2JAN2lVGcBalIBHwXzqjY/edit?usp=sharing). It helped me prioritize what aspects I needed to accomplish first and also helped identify features to descope into future releases. 
I attempted to follow a rough Agile methodology where I prefixed discovery tasks in Feature 0 for sprint 0. Then I used the following numbers as a hierarchy of what to develop first:

 | Epic Task Number 	|                         Tasks                        	|                                                                     Deliverables                                                                    	|
|:----------------:	|:----------------------------------------------------:	|:---------------------------------------------------------------------------------------------------------------------------------------------------:	|
|         0        	| Discovery & Design                                   	| Wire-frames<br>Colors<br>Fonts<br>Initial Data Model<br>List of Features                                                                            	|
|         1        	| UI Decisions                                         	| Identify Design Elements<br>Choose CSS Framework<br>Images<br>Base Layout<br>Navigation<br>Footer                                                   	|
|         2        	| Build UI Components                                  	| Star Input Rating<br>Age Multi Selector<br>Check Boxes<br>Date Picker<br>Icon Selector<br>Switches<br>Form Inputs<br>Deploy to Local                	|
|         3        	| Accept User Inputs<br>DB Interaction                 	| Address Collection<br>Event Collection<br>Place Collection<br>Review Collection<br>Write to mongodb<br>Read from mongodb<br>Deploy to Heroku        	|
|         4        	| Rough list Places<br>List Events<br>Join Event Layer 	| Maps<br>Update mongodb<br>Email<br>aggregated mongo queries<br>google calendar                                                                      	|
|         5        	| Filter Events                                        	| aggregated find queries<br>flask routes with parameters                                                                                             	|
|         6        	| Edit Events                                          	| Flask route<br>reusable code - macros<br>reusable code - filters                                                                                    	|
|         7        	| Update Event                                         	| Flask Route<br>Form Pre-population<br>add conditionals to db query                                                                                  	|
|         8        	| List Places                                          	| Accordions<br>aggregated star rating<br>Google Maps<br>tooltips<br>merge events, reviews                                                            	|
|         9        	| Add Review                                           	| Review Form<br>Refactor Code for Blueprint<br>Success/Fail modals                                                                                   	|
|        10        	| Testing                                              	| Identify Types of Testing<br>Write Test Cases<br>Execute Test Case<br>Automate Tests                                                                	|
|        11        	| Metrics                                              	| Devise Tracking Scheme<br>Hook up DB<br>Implement Click Tracking<br>Implement Page Tracking<br>Ajax Post Clicks<br>Routing<br>Rough Display of Data 	|
|        12        	| Documentation                                        	| Clean up Sections<br>Refactor into Smaller Files<br>Explain Decisions<br>Check Links<br>Check Images                                                	|
|        13        	| Finalize UI                                          	| Final Footer<br>Final Nav<br>Execute Cross Browser Tests<br>Execute Accessibility Tests                                                             	|
|        14        	| Refactor                                             	| Identify Reuse<br>Clean up unused files<br>Restructure Directories<br>Test Deployment Instructions                                                  	|
|        15        	| Demo                                                 	| Peer Review<br>Mentor Meeting                                                                                                                       	|
 
 If you sort the Project Tracking sheet by Complete Date, you can see that I would finish about 80-90% of an epic task and then start working on another feature. This goes hand in hand with the agile development cycle where epic features are all intermingled due to the interdependency of the UI components.  It is definitely nice to see the completed count diminish.

## Technologies Used
### Programming languages
- [CSS3](https://www.w3schools.com/w3css/default.asp) - used to define DOM appearance. 
- [HTML5](https://www.w3schools.com/html/default.asp) -  used to define DOM elements. 
- [JQuery](https://jquery.com) - used to initialize elements of Bulma framework: check boxes, date pickers, menu toggles.
- [JavaScript](https://www.javascript.com/)  -  used to format dates and pull data from element attributes.
- [Python](https://www.python.org/) the project back-end functions are written using Python. Flask and Python is used to build route functions
- [Markdown](https://www.markdownguide.org/) Documentation within the readme was generated using markdown
### Framework & Extensions
- [Bulma](https://bulma.io/) - a mobile first, free, open source CSS framework based on Flex-box. Using this framework provides many nice top design elements such as navigation menu bar for desktop, side nav bar for mobile, modals/layers, containers and forms.
- [Bulma Extensions](https://wikiki.github.io/) extends Bluma by adding more complex design features such as: accordions, pagination, datetime pickers, checkradios, and switches.
- [mongodb](https://www.mongodb.com/cloud/atlas)- a fully-managed cloud database used to store manage and query data sets
- [Flask](https://flask-doc.readthedocs.io/en/latest/) - python based templating language. I used Flask for:
  - routing - passing database queries to templates for page specific presentations
  - layouts - extensions of templates for common layouts with prescribed blocks that can be customized
  - common elements - inclusion of HTML templates for common design elements like the navigation, footer, various forms
  - macros - to generate common HTML with variable dependent settings
- [WTForms](https://wtforms.readthedocs.io/en/stable/csrf.html#example) - form validation & form level cross-site request forgery protection
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/index.html)- extended form validation and global cross-site request forgery protection
- [Pygal](http://www.pygal.org/en/stable/documentation/) - charting for metrics dashboard
- [unittest](https://docs.python.org/3/library/unittest.html) - testing database CRUD functions, flask routing
- [google sheets & drive](https://drive.google.com/drive/folders/1mYY4M0jXf6sPWesmP9Q-wFvjpgT1v8IU?usp=sharing) - Used to create testing documents and project plan (feature to do list) 
### Fonts
- [FontAwesome]() - for icons associated with buttons and inputs
- [Patrick Hand SC](https://fonts.google.com/specimen/Patrick+Hand+SC) - Google Font's Patrick Hand font was used for headers and home page dialog
- [Raleway](https://fonts.google.com/specimen/Raleway) - Google's Raleway font was used as the main font
### Tools
- [draw.io](https://about.draw.io/features/) - used to create Entity Relationship diagrams.
- [balsamiq](https://balsamiq.com/) - used to create professional looking wire frames.
- [markdown table generator](https://www.tablesgenerator.com/markdown_tables) - used to help with documentation table formatting
- [icon generator](https://favicon.io/favicon-generator/) - free site to help in website icon generation
- [regex101.com](https://regex101.com/) - used to help fine tune some regular expression based validation
- [github](https://github.com/) - used for version control of project files
- [heroku](https://www.heroku.com/) - runs the what2do2day application in the cloud
- [color contrast](https://webaim.org/resourceshttps://webaim.org/resources/contrastchecker//contrastchecker/) Tool was used to adjust colors on fonts flagged as needing a higher contrast ratio from google's lighthouse audit tool.
- [lighthouse audit](https://developers.google.com/web/tools/lighthouse) Google's open source automated too to help improve the quality of your website. Specifically paid attention to Accessibility  and best practices aiming for scores above 80.
### APIs
- [stmp](https://github.com/python/cpython/blob/3.8/Lib/smtplib.py) - Send user notices when an event is joined or when an event they have joined has been updated.
- [Google Maps Javascript API](https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/javascript/examples/) - Customized Map of event and places

## Testing
Constant integration testing was preformed to ensure no console/javascript errors were present. Beyond that, unit testing, validation testing, cross browser testing, accessibility testing, and regression testing were manually performed. I also explored automated testing of custom filters that I created. Ideally mocked up database functionality tests would be automated as well, but I have not yet found the time to learn how to mock database data.

### Validation Testing
I used the following validation websites to test the code:
- [CSS Validator](https://jigsaw.w3.org/css-validator/) Note, any error associated with root: color variables were ignored. Vendor extension warnings were also ignored. Bulma extension CSS errors concerning SVG and text area visibility were ignored too.
- [HTML Validator](https://validator.w3.org/)  - validation of HTML with FLASK is pretty useless as all {{}} bracketed values raise errors. I ran only a few files through the validator and instead relyed heavily upon pycharm's IDE to identify mismatched tags and closing Flask directives.
- [JSON Validator](https://jsonlint.com/) Used to validate roughed in json-ld for future google calendar integration. It is part of the user send invite email currently, but does not seem to be picked up by gmail. Note: warnings were ignored.
- [JavaScript Validator](http://beautifytools.com/javascript-validator.php) Note any errors for let, variables set in other .js files, and constants were ignored. I also used a more [ES6 friendly checker](https://www.piliapp.com/syntax-check/es6/) and there were no errors for main.js

### Unit Testing
To ensure core functionality and features were delivered and working I created a series of manual tests in a [google doc](https://docs.google.com/spreadsheets/d/1p1aoEQsVZUAZN50AQLZbaerS9UVVQkHG--XoiNccaC0/edit?usp=sharing)
These manual unit test cases focus on testing the core functionality in a desktop browser only and examining the console for errors. Ideally the core functionality would be verified using mocked database inputs to the controller functions for specific views.

### Cross Browser/ Cross Device Verification
To verify that the application is functional and looks pleasant  across various operating systems and device sizes I devised another suite of manual tests in the cross browser tab of my [testing workheet](https://docs.google.com/spreadsheets/d/1p1aoEQsVZUAZN50AQLZbaerS9UVVQkHG--XoiNccaC0/edit?usp=sharing).
These tests are lighter on the functionality with more attention being paid to the layout and console logs.
The matrix for the browsers, operating systems and screen sizes is as follows:

|       TOOL      	|    DEVICE    	| BROWSER 	|    OS   	|   SCREEN WIDTH  	|
|:---------------:	|:------------:	|:-------:	|:-------:	|:---------------:	|
|       N/A       	|    motog6    	|  chrome 	| android 	| XS 360px & less 	|
|  browser stack  	|   iphone5s   	|  safari 	|   iOs   	| XS 360px & less 	|
| chrome emulator 	|    pixel 2   	| firefox 	| android 	|    M 361-576    	|
|   browserstack  	|  iPhone 10x  	|  Chrome 	|   iOs   	|    M 361-576    	|
|   browserstack  	|     nexus    	|  Chrome 	| android 	|  T-vert 571-768 	|
|       N/A       	|   ipad mini  	|  safari 	|   iOs   	|  T-vert 571-768 	|
|   browserstack  	|    galaxy    	| firefox 	| android 	|  T-hor 769-1024 	|
| chrome emulator 	|     ipad     	|  safari 	|   iOs   	|  T-hor 769-1024 	|
|   browserstack  	|       ?      	|  Chrome 	| windows 	|   HD 125-1240   	|
|       N/A       	| mac book pro 	|  safari 	|  Mohave 	|   HD 125-1240   	|
|   browserstack  	|       ?      	| firefox 	| windows 	|   HD 125-1240   	|
|   browserstack  	|       ?      	| IE Edge 	| windows 	|   HD 125-1240   	|

Another part of my cross browser testing was hitting each page in each view port with the chrome emulator and copying the following javascript  into the developer's tools console screen. 
```javascript
var docWidth = document.documentElement.offsetWidth;
[].forEach.call(document.querySelectorAll('*'),function(el){if(el.offsetWidth > docWidth){console.log(el);}});
```
This snippet grabs all elements in the DOM and outputs offending elements that exceed the width of the screen to the console. If the output is "undefined", then I can be 99% certain that users will not experience any odd horizontal scrolls on their devices.

### Cross Site Scripting and Forgery
During my unit testing I encountered the CSRF errors many times myself when I left the CSRF token off pages or update my routes to use blueprint and mistyped paths. This got me wondering what I can do to try to test my application proacively so I read [veracodes' XSS article](https://www.veracode.com/security/xss) article to figure out ways to manually test for XSS and CSRF.
Based on my findings I added a XSS sheet to my [testing doc](https://docs.google.com/spreadsheets/d/1p1aoEQsVZUAZN50AQLZbaerS9UVVQkHG--XoiNccaC0/edit?usp=sharing) And documented routes where url parameters are allowed as well as pages with text or text area entries and templating variables. I then attempted to inject scripting and forgeries into my website. I still don't think I know enough to be confident the site is safe, but it held up. {{TODO}}

### Accessibility Testing
Because I know a few people with both physical handicaps which makes using a mouse nearly impossible as well as a couple severely visually impaired people I try to ensure I build websites that can be use by them. I make use of  [axe](https://chrome.google.com/webstore/detail/axe-web-accessibility-tes/lhdoppojpmngadmnindnejefpokejbdd?hl=en-US) and [google's lighthouse audi](https://developers.google.com/web/tools/lighthouse) tool to help ensure that the application meets accessibility standards.

 
### Regression Testing
No one wants to keep running a large suite of unit tests and cross browser tests again and again. Due to my ineptitude at writing interactive tests with a database, I reduced the unit testing and cross site browsing testing to a smaller suite once the core development was 70% done. These tests are on the Regression Tests Tab of my [testing doc](https://docs.google.com/spreadsheets/d/1p1aoEQsVZUAZN50AQLZbaerS9UVVQkHG--XoiNccaC0/edit?usp=sharing). While I really want to mock some database interaction, I do not have the bandwidth to take on that additional learning at this time. 

### Automated Testing
I did install unittest and put tests around the custom filters I wrote as I do not want them breaking. Doing such pointed out several type flaws in my logic that I shored up.

These tests are in the [/tests/test_filters.py](https://github.com/maliahavlicek/what2do2day/blob/master/tests/test_filters.py) file.
From a terminal window you can execute this suite of test using the following command:
 ````$ python -m unittest tests/test_filters.py -v````
 
### Defect Tracking
Once I finished the initial layout of my file structure and had roughed in the base html, I began tracking [defects](https://docs.google.com/spreadsheets/d/161VXfe9ELN-CZMsHYaJfk8WoItRxhoAkscJhY_fMjdc/edit?usp=sharing) in a google sheet. They ranged from severely horrible coding errors, to the realization that my features were not 100% defined. 

#### Noteworthy Bugs
1. **500 CSRF** -One of the most intriguing bugs I encountered was a 500 error when I introduced page and click metrics. It took me a while to figure out how to restructure my ajax call through an onReady function out of base.html so I could easily access my CSRF_token and set it in the headers within the beforeSend function. Originally my ajax call was housed in my main.js file. That solution fixed 90% of the 500 errors I had seen, but I quickly discovered that my newer pages without forms lacked the setting of the csrf_token in a hidden form. It's easy to forget key steps if you take them early in the development process and forget about them a month later.
1. **flex block madness** Another odd bug was how my custom icon picker and multi picker for ages had mismatched heights. It took me a bit to discover a display flex on an outer div from 
1. **Bulma Date Picker** The most bamboozling issue I encountered was with Bulma's datepicker and form errors. The darned thing never preselected the date I previously had and had the wrong times. I trolled the internet and found that this is an exasperating issue for many hopeful bulma users. I ended up getting a have way working work around by modifying the calendar.js a bit and adding to my binding functions in main.js. This is the [official thread](https://github.com/Wikiki/bulma-calendar/issues/163#issuecomment-584172621) that I added my findings to in hopes of getting to a resolution. I tried switching my input field to a date but then it picked up some browser specific console logs so I switched it back to a datetime range.
1. **500 CSP google API** When testing with browser stack using safari iPhone6s I saw the following errors:
```
The source list for Content Security Policy directive 'script-src' contains an invalid source: ''strict-dynamic''. It will be ignored.
The source list for Content Security Policy directive 'script-src' contains an invalid source: ''report-sample''. It will be ignored.
```
Reading up on stack overflow it looks like google API wants you to have Content Security Policy directives. I tried append such to my flask app but that didn't work too well so I ended up adding many values to my base.html header and having to set a nuance value to my inline script. Learning so many things about web security.

#### Outstanding Defects



## Deployment
This site was developed using PyCharm's IDE. To keep records of different versions of all project files, git version control was used. This project is hosted using Heroku deployed from the master branch.

### GitHub
https://github.com/maliahavlicek/what2do2day

#### Requires
 - [Jinja](https://github.com/pallets/jinja) 
 ```$ pip install -U Jinja2```
 - [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) 
 ```$ pip install Flask-PyMongo```
 - MongoDB instance [downloaded and installed](https://docs.mongodb.com/manual/installation/)
 - MongoDB Atlas Cloud [URI connection string](https://docs.atlas.mongodb.com/driver-connection/) 
 ```mongodb+srv://user_name:password@cluster-pielp.mongodb.net/db_name?retryWrites=true&w=majority?```
 - [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/install.html) 
 ```$ pip install Flask-WTF```
 - A google api key [get here](https://developers.google.com/maps/documentation/javascript/get-api-key)
 - [flask-googlemaps](https://github.com/flask-extensions/Flask-GoogleMaps/blob/master/README.md) 
 ```$ pip install flask-googlemaps```
 - a [gmail accoount](https://accounts.google.com/signup) with less secure app access turned on use [this link](https://myaccount.google.com/lesssecureapps?pli=1) after you are signed into the gmail account

#### Running Locally
1. Get the code base from git hub by running this command in the terminal of your IDE: 
```$ git clone https://github.com/maliahavlicek/what2do2day.git```

2. [set environmental variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) with your own values for: 
> - MONGO_URI_WHAT2DO2DAY [URI connection string](https://docs.atlas.mongodb.com/driver-connection/) 
> - GOOGLE_MAP_KEY [get here](https://developers.google.com/maps/documentation/javascript/get-api-key)
> - SECRET_KEY - a long random string of bytes. For example, copy the output of this to your config:
                ```$ python -c 'import os; print(os.urandom(16))'```
> - WTF_CSRF_SECRET_KEY another long random string of bytes to help protect against cross site request forgery.  You can copy the output of this to your config:
                ```$ python -c 'import os; print(os.urandom(24))'```
> - EMAIL - a [gmail accoount](https://accounts.google.com/signup) once you have an account and are signed in you need to make sure it has less secure app access turned on use [this link](https://myaccount.google.com/lesssecureapps?pli=1)
> - EMAIL_PASS - the password to the email account

3. start your server by typing 
```$ python run.py```
4. load up the countries db from the helper file:
```$ python helpers/upload_countries.py ```
4. access your local version of the application at http://0.0.0.0:5000/home

### Heroku
Heroku can be used to run this site in a cloud environment to allow visibility to external users.
#### Deployment To Shared Environment
1. Get the code base from git hub by running this command in the terminal of your IDE: 
```bash
   $ git clone https://github.com/maliahavlicek/what2do2day.git
   ```
1. Login to Heroku and set up a new app
1. Under the **Settings** tab, click **Reveal Config Vars**
1. Set the following variables
> |        Variable       	|   Setting  	|
>|:---------------------:	|:----------:	|
>| IP                    	| 0.0.0.0    	|
>| PORT                  	| 5000       	|
>| MONGO_URI_WHAT2DO2DAY 	| YOUR_KEY  	|
>| SECRET_KEY            	| YOUR_KEY  	|
>| WTF_CSRF_SECRET_KE    	| YOUR_KEY  	|
>| GOOGLE_MAP_KEY        	| YOUR_KEY   	|
>| EMAIL                	| YOUR_KEY   	|
>| EMAIL_PASS            	| YOUR_KEY   	|

5. Go back to your IDE's terminal window and connect to heroku ```bash heroku login``` and enter your credentials
5. Clone the heroku repository (exact command can be found on the Deployment tab for the app you just created in heroku) ```bash heroku git:clone -a 'your_app_name'```
5. make a slight change to a file, say the readme.md file
5. add the files, commit and push to heroku master:
```bash
$ git add .
$ git commit -am "initial heroku commit" 
$ git push heroku master
```
You should be able to access the application at your heroku via the url provided in the terminal window, or the open app button from your heroku app dashboard.
Ex) https://what2do2day.herokuapp.com/

## Credits
- [Icons made by Freepik from www.flaticon.com](https://www.flaticon.com/packs/outdoor-activities-32)
- [tables in markdown](https://www.tablesgenerator.com/markdown_tables#)
- [star rating input](https://codepen.io/jexordexan/pen/yyYEJa) - Thanks Jordan-Simonds
- [toggle switch](https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_switch)
- [star rating display](https://codepen.io/FredGenkin/pen/eaXYGV) - Thanks Fred Genkin

### Content
- [Avanti Music](https://advantimusic.org) description and imagery

### Media
The photos used in this site were obtained from:

- [Aage icons](https://images.app.goo.gl/aed22uFkaURNm9we6) - baby, preschoolers, middle schoolers, high schoolers
- [More Age iIcons](https://images.app.goo.gl/kUcThrqJ6hLJHsBk9) - elementary, young adult, 21+
- [Activity Icons](https://www.flaticon.com/packs/outdoor-activities-32) made by Freepik and hosted at www.flaticon.com
- [Perry the Platypus](https://images.app.goo.gl/AbcvfgihqBk83TCu6) - secret agent platypus image used on list pages
- [Phineas and Ferb](https://images.app.goo.gl/upEMCarxtGChgSh5A) - used as background image on home page
- [grass](https://images.app.goo.gl/be322rrT66jYjYmq9) - cropped out a section of a backyard png, to have grass to underline title hero objects on pages
- [loading gif](https://images.app.goo.gl/WLbJdQc2PPEjFAaM7)- used to hold maps while they are retrieved from google API
- [success](https://images.app.goo.gl/ieQJ64nMJXXt7EMP9) - Phineas and Ferb jumping for joy image used on successful follow place, join event screens
- [opps](https://images.app.goo.gl/dtquPurPUkehqTGHA) - Doofensmirtz oooh image used for already joined, already followed, place already exists, event already exists screens
- [fixit](https://images.app.goo.gl/EVtxLRwobhduoVe66) - Ferb with tools used for 404, 500 errors where the page request doesn't exist or weird routing issues

### Acknowledgements
The wonderful results of the google search engine helped me tremendously in completing this project.
- [uniwebsidad.com](https://uniwebsidad.com/libros/explore-flask/chapter-8) - Provides documentation on more advanced features of flask
  - macros and include them from an external file 
  - how to make custom filters
- [speech bubbles](https://auralinna.blog/post/2017/how-to-make-a-css-speech-bubble-with-borders-and-drop-shadow) The home page dialog bubbles were adopted from this post by Tero Auralinna.
- [CSS tricks](https://css-tricks.com) has an assortment of helpful ways to use CSS to accomplish tasks. 
  - [image centering]((https://css-tricks.com/perfect-full-page-background-image/)) how to center the home page background image across device sizes
  -  [styling scrollbars](https://css-tricks.com/the-current-state-of-styling-scrollbars/) to conserve vertical space, I put the icon choices into a scrolling area, but wanted to show the scrollbars in an intuitive manner rather than relying on inconsistent default browser styles
- [Kyle Marek-Spartz](https://kyle.marek-spartz.org/posts/2014-04-04-setting-wtforms-selection-fields-dynamically.html) - Setting WTForms Selection Fields Dynamically
- [mcelhennyi](https://gist.github.com/devxoul/7638142) - Required If validation used in address, event, and review form entries
- [api_mongodb](https://api.mongodb.com/python/current/migrate-to-pymongo3.html) -  Help in overcoming and understanding write concern errors I encountered with mongodb
- [mongo reference](https://docs.mongodb.com/manual/reference/) - Learning how to manipulate dates, strings, perform lookups, sorting, and merges on data
- [javascript dates](https://www.aspsnippets.com/Articles/JavaScript-Display-Current-Time-in-12-hour-format-AM-PM-and-24-hour-format-with-Hours-Minutes-and-Seconds-hhmmss.aspx) to clean up date formatting in the initial count me in layer
- [Pretty Printed](https://www.youtube.com/watch?v=kWncnBBxoJ4&feature=youtu.be)This video shows how to integrate google maps to a python flask application.
- [aezel](https://stackoverflow.com/users/64266/aezell) for [posting](https://stackoverflow.com/users/64266/aezell) a good way to separate flask filters from run.py
- [Todd Birchard](https://hackersandslackers.com/flask-blueprints/) For a most useful example about blueprints to make a larger flask application's directory structure manageable
- [Dan Badar](https://dbader.org/blog/python-send-email)- how to send emails via python and a google account
- **the G-men** A special thanks goes out to my family for allowing me to ignore them for the past two months as I dove deep into unknown waters. I hope the new skills I'm gaining from this program can pay for us all to go visit the grandparents again. Hawaii or Croatia... tough decisions.
<img src="documentation/images/IMG_20190717_213729_096.jpg" width="300" height="auto" alt="picture of Malia's boys"/>
