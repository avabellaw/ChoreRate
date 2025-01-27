# ChoreRate

[View the live website here](https://chorerate-cb14d5db605d.herokuapp.com/login?next=%2F)

## Design

### Setup

### Features

* Each user rates chores.
  * Chores are then allocated each week based on ratings.
* Set frequency of chore (monthly, weekly, daily)
  * Set the times per frequency eg. 3x every week
  * Use this to to create schedule.
* Share less desirable chores.
* After rating chores, show what you've rated.
  * Replace "no more chores" message with this.
* Household chores can be backed up and even imported into new households.

#### Backend - How chores will be distrubuted

* Ratings are normalized
  * This levels out differences in ratings eg. if someone votes very high and very low vs someone voting in smaller differences.
* Distribution
  * Distrubuted so that chore duration total is equal for each member.
  * Each chore has a duration factor, duration / frequency (daily: 1, weekly: 7, monthly: 28).
  * Each user has a weighting created for each chore. This is rating * duration factor.
    * Starts with daily then weekly and monthly. 
    * Each members previously attributed weighting is taken in account after daily (the difference from the person with the heighest weighting).
  * Chores are distrubted to the highest possible equal member weighting.
    * Could use Python itertool.combination and take the highest most equal.
    * or by using linear programming optimisation
  * Chores are distributed in a way that prioritizes no one getting their least rated chore. Aims to get everyone the chores they want while balancing satisfaction.
* Each household member has a weighting
  * This is determined by duration * frequency of the chore and also how it was rated by the member.
  * This is so that weekly and monthly chores can be distrubed fairly.
    * This then covers cases where the number of chores don't divide nealty between the number of members.
  * A new member will receive the same rating as the member who has the lowest.

### User stories 

1. **User Registration and Login**
   * As a new user, I want to register for an account
   * As a registered user, I want to log in so that I can access my account and manage chores.

2. **Household Creation and Management**
   * As a user, I want to create a household so that I can become a household member.
   * As a household member, I want to add new users to my household as household members so that they can rate chores and be assigned them.
   * As a household member, I want to leave a household so that I am no longer part of it.
   * As a household member, I want to receive a warning when I am the last member trying to leave a household so that I'm aware the household will be deleted.

3. **Chore Management**
   * As a household member, I want to add new chores so that they can be assigned to household members.
   * As a household member, I want to edit existing chores so that I can update their details.
   * As a household member, I want to delete chores so that they are no longer part of the household's chore list.

4. **Chore Rating and Allocation**
   * As a household member, I want to rate chores so that the system can allocate chores based on preferences.
   * As a household member, I want to view my chore ratings so that I can see what I have rated.
   * As a household member, I want chores to be allocated each week based on ratings so that chores are distributed fairly.

5. **Chore Frequency and Scheduling**
   * As a household member, I want to set the frequency of chores (daily, weekly, monthly) so that they are scheduled appropriately.
   * As a household member, I want to set the times per frequency (e.g., 3x every week) so that chores are repeated as needed.
   * As a household member, I want to view the chore schedule so that I know when chores are due.

6. **Notifications and Reminders**
   * As a household member, I want to receive notifications when chores are due so that I don't forget to complete them.

7. **Household Backup and Import**
   * As a household member, I want to back up household chores so that I can restore them if needed.
   * As a household member, I want to import household chores into a new household so that I can reuse existing chore setups.

8.  **User Experience and Interface**
    * As a user, I want a user-friendly interface so that I can easily navigate and use the application.
    * As a user, I want to access the application on different devices (e.g., desktop, mobile) so that I can manage chores from anywhere.

### Sprints

#### User Registration and Login
* User registration form
* Backend logic for user registration
* User login form
* Backend logic for user login

#### Household Creation and Management
* Household creation form
* Backend logic for household creation
* Form to add new users to household
* Backend logic to add users to household

#### Chore Management
* Form to add new chores
* Backend logic to add chores
* Form to edit existing chores
* Backend logic to update chores
* Form to delete chores
* Backend logic to delete chores

#### Chore Rating
* Form to rate chores
* Backend logic to save chore ratings

#### Chore Allocated

* Algorithm to allocate chores based on ratings.
* Update the allocations monthly.
* Add a chore weighting to correctly balance chores.
  * For example, monthly chores may need to change user.
* Display allocated chores to users

### Wireframe

Wireframe created on Figma and [can be found here](https://www.figma.com/design/v2nJYg67szWzNOtYYGt84v/ChoreTool?node-id=1-2&t=HkiOzXU8oSLrsBJ6-1)


## Entity Relationship Diagram

ERD created on LucidChart and [can be found here](https://lucid.app/lucidchart/4fe510dc-91f4-4c66-9d34-28b186ccc122/edit?viewport_loc=-1173%2C-115%2C2742%2C1284%2C0_0&invitationId=inv_ef4eb648-4b5b-4cf5-b181-b8bd0e498cea)

## Enviroment variables

* DEBUG - _optional_ to set Flask debug to True
* IP - _optional_ to set the IP address of the server.
* PORT - _optional_ to set the port for the website.
* SECRET_KEY - the app's secret key to sign cookies and for encryption.
* DB_URL - Url for the database.

## Credit

### Images

* [Plus icon - by Pixel Perfect **Flaticon**](https://www.flaticon.com/free-icon/plus_1828819?term=plus&page=1&position=13&origin=search&related_id=1828819)

* [Minus icon - by Fathema Khanom **Flaticon**](https://www.flaticon.com/free-icon/minus_10263924?term=minus&page=1&position=14&origin=search&related_id=10263924)

* [Rate icon in logo and favicon - by photo3idea_studio **Flaticon**](https://www.flaticon.com/free-icon/rate_3163742?term=rate&page=1&position=1&origin=tag&related_id=3163742)
