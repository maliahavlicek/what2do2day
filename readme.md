# What2Do2Day
## Author
## Project Overview
This website provides people a way to find free events in their community as a means to solve the question of "What are we gonna do today?" without breaking the bank or needing to travel far from home. Along with finding inexpensive options of what to do today, the site allows users to flag that they are planning on attending an event so other members know they will not be the only one going to a function. 

Users can also see a list of all the places in the community that have ever hosted an event and read reviews about them. Users can add reviews about places to share their experiences and rate organizations. Places, Events, and Reviews can be added, deleted and updated from the site. If an activity doesn't quite fit into the list provided, users can add a new activity when creating an event or place. Small businesses, social groups, and communities would ideally be in charge of their organizations's data and events but in this beta phase, user authentication, roles and permissions are not implemented.

Site owners could enable affiliate linking from any organization associated with the site that results in a sale from the place's own website.  By adding a Google Click Identifier (GCLID) to a place's url when leaving What2Do2Day's site, offline conversions could be tracked and negotiated to a monetary value for the site owners. Site admins could also gather data based on search activity as well as Places and Events with heavy interaction and sell ads on this site to help earn money by targeting audiences of similar interests. (Note how the Places's page has natural side bars in desktop when users are looking at events and reviews, on mobile devices ad space could be inserted below filtering options and above the footer too.)

The name and concept of this site is loosely based on the key phrase, "I know what we're gonna do today!" from the cartoon series [Phineas and Ferb](https://en.wikipedia.org/wiki/Phineas_and_Ferb).
 
>## Table of Contents
> - [UX](#UX)
>   - [Strategy](#Strategy)
>   - [Scope](#Scope)
>   - [Structure](#Structure)
>   - [Skeleton](#skeleton)
>   - [Surface](#surface)
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
> - [Technologies Used](#technologies-used)
>     - [Programming languages](#programming-languages)
>     - [Framework & Extensions](#framework--extensions)
>     - [Fonts](#fonts)
>     - [Tools](#tools)
>     - [APIs](#apis)
> - [Testing](#testing)


## UX
### Strategy
Before launching any website, business partners want to know how they can earn money and if there is a need or demand for the project. Defining business goals of a project from the standpoint of an external user as well as site owners helps you evaluate possible return on investment.

Upon reading the suggested projects for the Data Centric Milestone Project, I came up with 2 ideas:

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
>  - Find something safe for your kids to do near home
>  - Find something that's interesting to me with others I know when mom and dad take away my electronics
>  - Bring Attention to your business or organization by being involved in the community
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

### Scope
The concept of What2Do2Day can get extremely intertwined when looking at permissions and roles. I decided that a beta version that skips over authentication, permissions and roles can still provide a clean and efficient minimal viable product (MVP).  Thus user profiles and management of users will not be included initially. 

Restricting results based on user's location would be ideal for a long term solution but it is not necessary for the MVP. Since I do not have experience with Google Maps's Nearby API, this bit of scope will be deferred until a polished core product is developed. Also not enough data will be loaded to make searching and geolocation viable initially.

Creating, adding and updating functionality will only be accessible from menu options. This will allow the MVP to be built to serve the majority of long term users and keep the UX cleaner without an overwhelming amount of buttons. Admin proximity/ease of use functionality can be added later. 

Consolidating Delete functionality into an enable/disable property reduces pages to develop. It also reduces the number of items in the menus and makes overall navigation easier.

Business logic to track search requests, and the events and places that users interact with will be collected.  This will aide in negotiating affiliate link deals and ads will be included but graphical visualization will not be included in the MVP, only a list of the data collected. Likewise we need to know how many users are coming to the site and what percentage of them interact or do not interact with out buttons so we will attempt to track unique visits to our site.

### Structure
In order to have a better idea of the tables and the relationships between them I looked at google Maps' Places API to help determine what fields my place object should have. Knowing the data fields I may want to have and those that were extraneous, helped me devise a rough Entity Relationship Diagram(ERD):
 ![Data Diagram](documentation/images/data_model/Data-Diagram-Initial.png)

After the decision to remove user roles and permissions and some refactoring around fields, I ended up with:

 ![Data Diagram](documentation/images/data_model/Data-Diagram.png)

### Skeleton
Having the data structure in hand, I knew what data fields I had at hand to present users managing the PLACES, EVENTS and REVIEW objects. I'm not a great artist but I find it easier start hand drawn markups before diving into a wireframing tool. I drafted out the home screen as well as the places list to kick start decisions concerning what data had higher priority.
[view hand drawn mockups](documentation/handdrawn.md)

Once I had the Places list drawn out, I invested several hours to mockup and fine tune the user experience using Basalmiq.
[view balsamiq deck](documentation/balsamiq.md)

Taking the time to do more formal mockups exposed an issue with the crowding of edit buttons and delete buttons. I decided that delete is really an update function since I am using the enabled attribute to hide or show items on the Places and Events pages.  The more formal mockups also allowed me to try several different layouts of the data for the main list pages. The mockkups include layers for searching and in site adding of reviews. Search non-happy paths were also mocked up. 

### Surface:
Below are the decisions and internal dialogs I had to help draw out what the end product will look like.
####Color Choice
I have not had much success with color choice in the past using online tools such as picking colors from imagery via adobe or from color pallet wheels. My color choices pass accessibility audits but something is missing, so this time, I started with the pros at [Sherwin Williams](https://www.sherwin-williams.com/homeowners/color/find-and-explore-colors/paint-colors-by-family/SW6790-adriatic-sea#/6790/?s=coordinatingColors&p=PS0) and came up with the following colors:

![colors](documentation/images/colors/AdriaticBlueCoordinatingColors.png)

I then went to dribble.com and plugged in each of the colors from  Sherwin Williams to find others' pallets that had a cheerful look. Unfortunately Adriatic Blue, Aesthetic White, and Felted Wool all provided me with rather depressing options. Luckily Bravo Blue(\#d3e7e9) turned up a lot of more cheerful looking sites.
- [One nice day](https://dribbble.com/shots/9428106-Vector-illustration-One-nice-day)
- [Online Learning App](https://dribbble.com/shots/9404019-Online-Learning-App)
- [Daily UI 004](https://dribbble.com/shots/9423898-Daily-UI-004)
- [Sign up](https://dribbble.com/shots/9404019-Online-Learning-App)

So I'm hoping I'll have success with the Daily UI 004 color's pallet.

![Color Pallet](documentation/images/colors/colorpallet.png)


#### Typography
The home page lends itself to a comic strip so I searched Google's handwriting fonts and flagged the top 5 that matched what I had envisioned and typed some example lead text.
- [WalterTurncoat](https://fonts.google.com/specimen/Walter+Turncoat)
- [Sriracha](https://fonts.google.com/specimen/Sriracha)
- [Coming Soon](https://fonts.google.com/specimen/Coming+Soon)
- [Caveat Brush](https://fonts.google.com/specimen/Caveat+Brush)
- [Patrick Hand SC](https://fonts.google.com/specimen/Patrick+Hand+SC)

In my opinion, the Patrick Hand SC font presented itself perfectly for cartoon writing when typing out potential lead text. It was easy to read and I could discern where true capitalization was and saw a difference between capital I's followed by lower case L's.

Next I produced a short list of fonts for my main content by looking at google's suggested pairings of fonts with Patrick Hand SC a list of [best fonts](https://kinsta.com/blog/best-google-fonts/):

- [Lato](https://fonts.google.com/specimen/Lato)
- [Open Sans](https://fonts.google.com/specimen/Open+Sans)
- [Raleway](https://fonts.google.com/specimen/Raleway)

While Open Sans matched the curvy flowing fonts which I was trying to achieve with for my main content, I could not distinguish a capital I from a lower case l, so I chose Raleway as it met that criteria. I don't plan on using many different font weights so I only imported those for normal and bold.

`<link href="https://fonts.googleapis.com/css?family=Patrick+Hand+SC&display=swap" rel="stylesheet">`
`<link href="https://fonts.googleapis.com/css?family=Raleway:500,700&display=swap" rel="stylesheet">`

#### Image Choice
I wanted easily recognizable activities as icons that users could use to associate to events and places on my website rather than allowing them to randomly load garish or naughty symbols, I decided to provide a broad set of icons. I looked at free sets and downloaded icons from [flaticon](https://www.flaticon.com/packs/outdoor-activities-32)
By having icons that are compatible with the colors I plan on using throughout my site, I am hoping to achieve a calm yet cheerful website. 

<img src="static/assets/images/icons/002-football-field.svg" width="50" height ="50"/>

#### Design Elements
The formal wireframe process identified the need for:
 - top menu bar for desktop
 - side nav bar for mobile
 - modals/layers
 - accordions
 - containers
 - pagination
 - forms
 - maps
 - rating selector
 - buttons
 - date pickers
 - select choice/drop downs
 - text input
 - text area inputs
 - checkboxes
 - switches
 - icon selection
 
 I did not want to invent all of the above, so I read [best css frameworks]('https://www.creativebloq.com/features/best-css-frameworks') to help make an informed decision on what framework to use. Foundation, picnic, and bulma made my short list as they appeared light weight and were frameworks I did not get exposure to from previous milestone projects or coursework. After reading up a bit, I decided that Bulma was the best fit for what I hoped to include in this project.

#### Animations & Transitions
I trolled codrops to look for some inspiration.  The following sites gave animation ideas that greatly altered my original wireframes:
 - [expanding search option](https://tympanus.net/Tutorials/ExpandingSearchBar/) 
 - [grid icon expansion](https://tympanus.net/codrops/2013/03/19/thumbnail-grid-with-expanding-preview/)
 - [expanding overlay](https://tympanus.net/Tutorials/ExpandingOverlayEffect/)
 - [fullscreen overly](https://tympanus.net/Development/FullscreenGridPortfolioTemplate/)

By seeing live examples, it dawned on me that I could have a small icon or minimal data in my list instead of the kitchen sink. I went back to my designs reduced the amount of data seen on the events and places lists pages so the user can see more options at one time. I hope to then enable clicking on a row to expand out to full screen and present all the data needed with a friendly animation.
 
### User Stories:
This website serves 3 sets of users, thus the stories are broken down into 3 categories:

### For kids looking for something free to do today in their neighborhood:
  - As a user, I'd like a list of events happening.
  - As a user, I want to filter events by age and activity so I can find something to do that matches my interests.
  - As a user, I want to sort events by a date range so I can find something to do in the future easily.
  - As a user, I want to join an event so I can be reminded when it happens.
  - As a user, I want to follow a place that hosts events so I can know when a new event is added immediately.
  - As a user, I want to read reviews about places that host events, so I know what to expect.
  - As a user, I want to write a review about a place so I can share my opinion.
  - As a user, I want to remove my review about a place so I can have a low profile online.

#### For places and organizations involved in building the community
  - As a user, I want to list my place so the community knows about it.
  - As a user, I want to have honest reviews about my place to build trust with the community.
  - As a user, I want to remove reviews about my place so that inappropriate comments are not associated with my place.
  - As a user, I want people to follow my place so they can know about events, and so I can compare my place to other places that host similar activities.
  - As a user, I want to add events to my place so the community knows about them.
  - As a user, I want people to join my events, so I can communicate with them if details change and plan for the right number of people.
  - As a user, I want to disable my events if the weather doesn't cooperate.
  - As a user, I want to disable my place if I decide to retire, go on vacation, or sell my place.

#### For site owners hosting a website to store community information
  - Home page that communicates the purpose of the website
  - ability to track search criteria to better sell ad space
  - ability to track places users follow to negotiate offline conversion money
  - ability to track events users join to negotiate offline conversion money and to better target ads
  - ability to track reviews uses write to better gauge community engagement
  - ability to track user's emails for research purposes in beta, potential marketing in the future

## Features
To streamline the development process without the complexity of user roles and permissions, it was decided that the MVP consists of a beta product as a proof of concept for a small market. The beta features are those listed in the Implemented Features. If the project is taken to it's full potential, the Features Left to Implement would be tackled.

### Implemented Features
#### Structural
1. Navbar - the navbar stays collapsed on medium and small devices. The navbar contains brand logo and links to associated sections i.e. Home, Events, Places, Contribute Update. Bulma's navbar implementation was used.
1. Footer - contains disclaimer, copyrights information, links to github repository and developer's resume
#### Common Elements
1. Speech Bubble - used on home page to inform users what the site is about
1. Icon buttons - used to indicate adding events, adding places, adding reviews, following places, joining events
1. Switches - enabling and disabling events, places and reviews
1. Date Pickers - setting up time frames of events
1. Rating Selector - star icon based radio button to record user ratings
1. Overlays - way to disable main page while getting user input for filtering results, joining an event, following a place, add review
1. Checkboxes - user friendly way to hide/show sections such as place address, place add event, place add review, event address
1. Icon Selector - when feels a different activity is needed, they can pick from a list of icons to associate the activity to
1. Accordion - collapse places' reviews and events, expand on click
1. Pagination - when results for events or places pages exceed 10, paginate results
#### Forms
1. Add Place - validation for required fields and proper data, unique Name check
1. Update Place - validation for required fields and proper data, uniqueness check
1. Add Event - validation for required fields and proper data, unique Name and Date check
1. Update Event - validation for required fields and proper data, uniqueness check
1. Add Review - validation for required fields
1. Update Review
#### Data Operations
1. Aggregated Review - from enabled reviews of a given place, present an average rating for a place
1. Count of followers - When a unique email is entered, add them to follower list
1. Count of event joiners - When a unique email is entered, add them to the joiner list
#### API Integration
1. Email JS - when an event is added to a place, email details to followers
1. Google Calendar - when a user joins an event, send calendar invite, when event is updated, email joiner list
1. Google Maps - show map of event location, show map of place location
#### Metrics
1. track follows by place and activity type
1. track joins by event and activity type
1. track searches by activity and age inputs
1. track places in db by activity type
1. track events in system by activity type
 
### Features Left to Implement
In the long term once this concept proves viable, authentication would be enabled and five sets of roles would accessing the site: 
#### User Roles & Permissions
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
#### API Integrations
1. GoogleAds - ad placement, offline conversions, automatic bidding
1. GoogleMaps Sitepoint - get directions from current location
1. GoogleMaps Geolocation - share location with other members, narrow results of events and places by proximity


## Technologies Used
### Programming languages
- [CSS3](https://www.w3schools.com/w3css/default.asp) - used to define DOM appearance. 
- [HTML5](https://www.w3schools.com/html/default.asp) -  used to define DOM elements. 
- [JQuery](https://jquery.com) - used to initialize elements of Bulma framework: check boxes, date pickers, menu toggles.
- [JavaScript](https://www.javascript.com/)  -  used to implement Maps JavaScript API, Calendar API, and EmailJS.
- [Python](https://www.python.org/) the project back-end functions are written using Python. Flask and Python is used to build route functions
- [Markdown](https://www.markdownguide.org/) Documentation within the readme was generated using markdown
### Framework & Extensions
- [Bulma](https://bulma.io/) - a mobile first, free, open source CSS framework based on Flex-box. Using this framework provides many nice top design elements such as navigation menu bar for desktop, side nav bar for mobile, modals/layers, containers and forms.
- [Bulma Extensions](https://wikiki.github.io/) extends Bluma by adding more complex design features such as: accordions, pagination, datetime pickers, checkradios, and switches.
- [mongodb](https://www.mongodb.com/cloud/atlas)- a fully-managed cloud database used to store manage and query data sets
- [Flask](https://flask-doc.readthedocs.io/en/latest/) - python based templating language that helps developers re-user HTML templates.
- [Pygal](http://www.pygal.org/en/stable/documentation/) - charting for metrics dashboard
- [unittest](https://docs.python.org/3/library/unittest.html) - testing database CRUD functions, flask routing
### Fonts
- [FontAwesom]() - for icons
- [Patrick Hand SC](https://fonts.google.com/specimen/Patrick+Hand+SC) - Google Font's Patrick Hand font was used for headers and home page dialog
- [Raleway](https://fonts.google.com/specimen/Raleway) - Google's Raleway font was used as the main font
### Tools
- [draw.io](https://about.draw.io/features/) - used to create Entity Relationship diagrams.
- [balsamiq](https://balsamiq.com/) - used to create professional looking wire frames.
- [markdown table generator](https://www.tablesgenerator.com/markdown_tables) - used to help with documentation table formatting
- [icon generator](https://favicon.io/favicon-generator/) - free site to help in website icon generation
### APIs
- [emailJS](https://emailjs.com) - Send user notices when place they are following is modified, has a new event, or has a new review posted. 
- [Google Calendar API](https://developers.google.com/calendar/v3/reference/events) - Used to [create events](https://developers.google.com/calendar/create-events) for application, add attendees when users join an event, and send updates to joiners if event is modified
- [Google Maps Javascript API](https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/javascript/examples/) - Customized Map of event and places

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
[Icons made by Freepik from www.flaticon.com](https://www.flaticon.com/packs/outdoor-activities-32)
[tables in markdown](https://www.tablesgenerator.com/markdown_tables#)
[star rating input](https://codepen.io/jexordexan/pen/yyYEJa)
[toggle switch](https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_switch)

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X
- I found out how to make macros and include them from an external file from [uniwebsidad.com](https://uniwebsidad.com/libros/explore-flask/chapter-8/creating-macros)
- [speech bubbles](https://auralinna.blog/post/2017/how-to-make-a-css-speech-bubble-with-borders-and-drop-shadow) on the home page were adopted from this post by Tero Auralinna.
- [home background](https://css-tricks.com/perfect-full-page-background-image/) centering technique via CSS

