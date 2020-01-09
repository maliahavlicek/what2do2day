<div class="myWrapper" markdown="1">
# What2Do2Day
This website provides people a way to find free events in their community as a means to solve the question of "What are we gonna do today?" without breaking the bank or needing to travel far from home.

Along with finding inexpensive options of what to do today, the site allows users to flag that they are planning on attending an event so other members know they will not be the only one going to a function.
 
Users can also see a list of all the places in the community that have ever hosted an event and read reviews about them. Users can add reviews about places to share their experiences. Places, Events, and Reviews can be added, deleted and updated from the site. If an activity doesn't quite fit into the list provided, users can add a new activity when creating an event or place.

Small businesses, social groups, and communities would ideally be in charge of their organizations's data and events but in this beta phase, user authentication, roles and permissions are not implemented.

Site owners could enable affiliate linking associated with promos from any organization associated with the site that results in a booking for paid events. Site admins could also gather data based on search activity as well as Places and Events with heavy interaction and sell ads on their site to help earn money.

The name and concept of this site is loosely based on the key phrase, "I know what we're gonna do today!" from the cartoon series Phineas and Ferb.

[![Phineas and Ferb](Documentation/readme/PhineasAndFerb.jpg)](https://en.wikipedia.org/wiki/Phineas_and_Ferb)
 
## Author
Malia Havlicek

## UX
### Strategy:
The first step of any UX Project is defining business goals of a project.

Upon reading the suggested projects for the Data Centric Milestone Project, I came up with 2 ideas:

1.Texting Translator:
> External Goals
>  -  Lookup definitions so you know what LOL and MILF means before determining if you need to have  serious talk with your children
>
> Site Owner's Goals
>  - Publish T-shirts, & stickers mugs for benign but up to date trends
>
> Features
>   - Forms that allows users to Add , Edit , Delete, Search Texting Terms   
>   - Up and Down voting if Definition is Good, BAD, AWFUL
>   - Metrics about what words were search for the most so owner can Stock Online store accordingly

2.What2Do2Day:
> External Goals
>  - Find something safe for your kids to do near home
>  - Find something that's interesting to me with others I know when mom and dad take away my electronics
>  - Bring Attention to business or organization by being involved in teh community
> Site Owner's Goal
>  - Earn $ from affiliate links to businesses that post their places on site when links lead to online sales
>  - Track most popular activities on site to score some $ from ads
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
<p style="text-align: center;">Texting Translator</p>
|             Pros              |                        Cons                        |
|-------------------------------|----------------------------------------------------|
| MVP could go live             | Rather Simple                                      |
| Moderate  UX                  | No API integration                                 |
| Scalable to world market      |                                                    |
| Ad and product placement high |                                                    |

<p style="text-align: center;">What2Do2Day</p>
|             Pros              |                        Cons                        |
|-------------------------------|----------------------------------------------------|
| Integration with Google Maps  | Very complex                                       |
| Challenging UX                | MVP not production worthy, anyone can make updates |
| Scalable to world market      | MVP not production worthy, (kid safety first)      |
| Ad potential is high          |                                                    |

 What2Do2Day has the ability to reach a broader scope of users and could potentially take off like the Nextdoor app.  What2Do2Day is more intriguing and likely to keep me coming back to the site as a user. As a developer, the What2Do2Day app will provide greater value in the long term towards my coding skills due to it's complexity.

### Scope & Strategy:
The concept of What2Do2Day can get extremely intertwined when looking at permissions and roles. I decided that a beta version that skips over authentication, permissions and roles can still provide a clean and efficient minimal viable product (MVP).  Thus user profiles and management of users will not be included initially. 

Restricting results based on user's location would be ideal for a long term solution but it is not necessary for the MVP. Since I do not have experience with Google Maps's Nearby API, this bit of scope will be deferred until a polished core product is developed. Also not enough data will be loaded to make searching and geolocation viable initially.

Creating, adding and updating functionality will only be accessible from menu options. This will allow the MVP to be built to serve the majority of long term users and keep the UX cleaner without an overwhelming amount of buttons. Admin proximity/ease of use functionality can be added later. 

Consolidating Delete functionality into an enable/disable property reduces pages to develop. It also reduces the number of items in the menus and makes overall navigation easier.

Business logic to track search requests, and the events and places that users interact with will be collected.  This will aide in negotiating affiliate link deals and ads will be included but graphical visualization will not be included in the MVP, only a list of the data collected. Likewise we need to know how many users are coming to the site and what percentage of them interact or do not interact with out buttons so we will attempt to track unique visits to our site.

### Structure:
In order to have a better idea of the tables and the relationships between them:
 ![Data Diagram](Documentation/readme/Data Diagram.png)
I looked at google Maps' Places API to help determine what fields my place object should have. Knowing the date and the relationship helped me refine the data and take it down to its MVP form.

### Skeleton:
Having the data structure in hand, I know what I need to present users managing the PLACES, EVENTS and REVIEW objects. I'm not a great artist but I find it easier start hand drawn markups as my proficiency with UX tools is lacking and I'm very reluctant to pony up money for a license.
[view hand drawn mockups](Documentation/handdrawn.md)

After noticing Code Institute partnered with Balsamiq, I invested several hours to mockup and fine tune the user experience:
[view balsamiq deck](Documentation/balsamiq.md)

Taking the time to do more formal mockups exposed an issue with the crowding of edit buttons and delete buttons. I decided that delete is really an update function since I'm using the enabled attribute to hide or show items on the Places and Events pages.  The more formal  mockups also allowed me to try several different fits and layouts of the data for the main list pages. So while not proficient, I am learning the importance as it draws out a more definitive user experience.  I added layers for filtering and in site adding of reviews. 


#### user stories
1. Home
1. Navigation
1. Events List
> As a kid bored out of my mind, I want to find something cheap to do that is nearby so I can be around others doing something other than online gaming without bugging my parents who are busy working.
1. Places
1. Edit Places
1. Edit Events
1. Edit Review - take user to Edit Places Page
1. Add Place
1. Add Event - take user to Edit Places Page
1. Add Review - take user to Edit Places Page
1. Delete Place - take user ot Edit Places Page
1. Delete Event - take user to Edit Places Page
1. Delete Review - take user to Edit Places Page
- Pagination of results, only show a max of 10 results per page.
- 
- Filter Places by activity and age.





### Surface:

####Color Choice
https://www.sherwin-williams.com/homeowners/color/find-and-explore-colors/paint-colors-by-family/SW6790-adriatic-sea#/6790/?s=coordinatingColors&p=PS0

#### Typography
 https://uxplanet.org/10-tips-on-typography-in-web-design-13a378f4aa0d

#### Image Choice
https://www.flaticon.com/packs/outdoor-activities-32

#### Design Elements

#### animations/Transitions
materialize or bootstraps

####

#### User Stories:

Use this section to provide insight into your UX process, focusing on who this website is for, what it is that they want to achieve and how your project is the best way to help them achieve these things.

In particular, as part of this section we recommend that you provide a list of User Stories, with the following general structure:
- As a user type, I want to perform an action, so that I can achieve a goal.

This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included as a pdf file in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.

## Features

In this section, you should go over the different parts of your project, and describe each in a sentence or so.

To streamline the development process without the complexity of users and permissions, it was decided that the MVP consists of:
1. Home Page: What are we going to do today screen. Explains purpose of site and includes 2 buttons for Events and Places lists.
1. Places Page:  User sees a list of enabled places. Search functionality for City, State Country, Rating and Activity will be present to reduce results and compensate for no geolocation. Track Activity Search inputs. Track expansion of details and reviews of Places. Allow pagination.
1. Creating Place Page: User inputs values where adding a review and an event are part of the process but not necessarily required. A warning will be provided if the name is found in existing database.
1. Update Place Page: User is presented a find field that will list 5 results with update options including disabled ones. List enabled Places first. If no match found, users can add a place or revise their search criteria. Once the update button is clicked, the user is presented with a form prepopulated with the Place's existing data. Aggregated rating values is visible but cannot be updated. Reviews associated with the place are presented in a list, cannot be managed from this screen. MVP dictates that ease of use/proximity of managing reviews is not essential to initial deployment.
1. Delete Place Page: User is presented a Name find field that will list 5 results of enabled places with delete options. Once a delete button is clicked, the place will be disabled and user will be taken to places list page. Deleted Places will just disable items to prevent user from having to reenter data if the Place is moving locations or undergoing maintenance.
1. Events Page: Display all future events to user ascending by date. Include ability to limit results by City, State Country, Activity to compensate for no geolocation. Track Activity Search inputs. Track expansion of details and count me in interaction. Allow pagination.
1. Create Event Page: User is presented an input field for the place's name it is associated with. If no matches found they can opt to create a place. If matches are found enabled items are listed first. Limit results to 5. Once the create event button is clicked, the user is shown a from to create an event. A warning will be provided upon submit if the Date and Title match an existing event for that Place.
1. Update Event Page: User is presented a find field for the place's name, date and activity to aid in finding the event.  If no matches found they can update their search criteria. If matches are found enabled items are listed first, allow pagination of results. Once the update button is clicked, the user is shown a from prepopulated with the existing entries. Upon submit, the Event's Name and Date is checked against existing events
for the place and the user is warned if a match is found. If no warning, the database is updated and user is returned to the Places page with results limited to that Place. 
1. Deleting Event Page:  User is presented a find field for the place's name, date and activity to aid in finding the event.  If no matches found they can update their search criteria. If matches are found only enabled items are listed. Allow pagination of results. Deleting only disables an event. Once user clicks Delete button, they are returned to the Delete Event Page.
1. Create Review Page: User is presented a find field for the place's name to aid in finding the Place.  If no matches found they can update their search criteria. Only show matches for enabled Places. Limit results to 5.
1. Update Review Page: User is presented a find field for the place's name to aid in finding the Review.  If no places are found they can update their search criteria. Show matches for both enabled and disabled Places, listing enabled first. Limit results to 5. Once a Place is picked, the reviews associated for that Place are listed with enabled first and disabled second. Pagination of results is allowed. Once an update button is clicked, the user is presented with a form field prepopulated with the review's current entries. Clicking the submit button updates the review and takes the user back to the update review page.
1. Delete Review Page: User is presented a find field for the place's name to aid in finding the Review..  If no matches found they can update their search criteria. Show matches for enabled and disabled Places, listing enabled first. Limit results to 5. Once a place is selected, present the user with enabled reviews for that place. Clicking Delete only toggles Review to disabled, return user to Places Page.
1. Create Activity Screen: When creating an event or place, the activity specific to the place may not exist. Only on Add/Update screens of Place or Event will there be a button to access this functionality exist. When clicked the create Activity button exposes two more form fields and hides the Activity drop down. This allows the user to add an activity icon and name. Submitting a Place or Event with these fields exposed will create a new Activity.
1. Navigation

 
### Features Left to Implement
In the long term once this concept proves viable, authentication would be enabled and five sets of roles would accessing the site: 
- <strong>Place Administrators</strong> -  users who have permissions to manage the Place, Events and Activities.
- <strong>External Users Adults</strong> - users who have permissions to grant minor external users  access to the site. Adult users
would also have permissions to manage their profile and create, edit and delete their own reviews.
- <strong>External Users Minors</strong> - users who must be granted permissions to the site by Adult External Users.
Minor users can manage their profile with limited features to help ensure their safety (no images or location settings if
and when those features are added to the site). Minor users can also create, edit and delete their own reviews.
- <strong>Content Admins</strong> -  users who approve reviews for inappropriate content and bot induced batch reviews. Content admins would
also be in charge of setting up ad campaigns.
- <strong>Site Administrators</strong> - users who have permissions to create, update and delete all the data hosted on the site 
(Users, Places, Events, Reviews

## Technologies Used
- [draw.io](https://about.draw.io/features/) - used to create Entity Relationship diagram.
- [balsamiq](https://balsamiq.com/) - used to create more professional mock ups.
- [markdown table generator](https://www.tablesgenerator.com/markdown_tables) - used to help with documentation table formatting
- [JQuery](https://jquery.com)- The project uses **JQuery** to simplify DOM manipulation.



## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X

</div>