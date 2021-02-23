# API Wars

The site provides data about the planets, with lots of details, from
the Star Wars Universe. 

![Register](/img/register.png 'Register')

The logged in user can vote (new button appears on the "vote"
column) a planet.

![Planets](/img/planets.png 'Planets')

There is a button to examine the Star Wars characters that come
from a specific planet.

![Residents](/img/residents.png 'Residents')


May the Force be with you!



## Story

Because you are so awesome, a golden humanoid droid want to meet you in the
nearest Kantina....

[Watch this
intro!](https://starwarsintrocreator.kassellabs.io/?ref=redirect#!/BM1kT5Ezi0Q0b-Ell8TE)

Your task is to create a little web application which shows data about the Star
Wars universe, store visitor preferences with cookies and handle user login with
sessions.

## What are you going to learn?
- create a Flask project,
- use routes with Flask,
- use Bootstrap,
- use AJAX for API requests,
- session handling,
- simple queries in SQL,
- password storage.

## Tasks


1. Create a web server rendering a page that shows a table with all the planets in the Star Wars universe.

    - The opening page of the website (`/`) shows data of 10 planets
    - The page has an HTML `<table>` element containing the data
    - The columns of the table are `name`, `diameter` (shown in km), `climate`, `terrain`, `surface water` (shown as percentage), `population` (formatted as `1,000,000 people`)
    - The column titles are proper table headers
    - There's a next button above the table, clicking that shows the next 10 planets, if any
    - There's a previous button above the table, clicking that shows the previous 10 planets, if any
    - Double clicking on the next or previous buttons shows the next/previous 10 planets only once
    - Unknown values for surface water percentage and population are stated clearly and without any suffix (e.g for planet Coruscant and Hoth)

2. Display a button in each row if the planet has residents. These buttons should open a modal, populate its data containing the list of residents with more detailed information.

    - In the planet table there is a button in each row in a new column showing the planet's number of residents if the planet has any, otherwise the `No known residents` text is shown
    - Clicking the `<n> residents` button in the planet table, a modal shows up showing all the residents of that planet (every time)
    - The modal has an HTML `<table>` element containing the data
    - The columns of the table are `name`, `height` (shown in meters), `mass` (shown in kg), `skin color`, `hair color`, `eye color`, `birth year`, `gender` (an icon representation)
    - Data is loaded into the table without page refresh (with AJAX)
    - There is an X icon in the top right corner and a `Close` button in the bottom right corner; clicking these closes the modal


3. Create a simple user login system with registration page, login page and logout link in the header.

    - There is a link in the header that leads to the registration page
    - On the registration page (`/register` route) the visitor can create a username/password pair that gets stored in the database
    - Password storage and retrieval uses salted password hashing for maximum security
    - If either field is empty while clicking on the `Submit` button on the registration page the `Please, fill in both fields.` error message appears
    - If the username field contains a username that already exists in the database while clicking on the `Submit` button on the registration page the `Username already exists, please choose another one!` error message appears
    - On successful registration the `Successful registration. Log in to continue.` text is shown and the user is redirected to the login page
    - There is a link in the header that leads to the login page
    - On the login page (`/login` route) the visitor can log in using the username/password previously created during registration
    - If the username/password pair doesn't match while clicking on the `Submit` button on the login page the `Wrong username or password.` error message appears
    - After logging in, the username is displayed in the top right corner with the text `Signed in as <username>` and a logout link is shown in the header
    - Clicking the logout link (`/logout` route) logs the user out

4. [OPTIONAL] If the user is logged in, display a button in each row with which the logged in user can vote on a planet. Save this vote in a database and inform a user that the vote has been saved.

    - If the user is logged in, a `Vote` button is displayed in the planet table in a new column
    - Clicking the vote button saves the vote in the database without refreshing the page (with AJAX)
    - If the save is successful after clicking the vote button, the `Voted on planet <planetname> successfully.` message appears
    - If the save is failed after clicking the vote button, the `There was an error during voting on planet <planetname>.` error message appears
    - Users can vote on unlimited number of planets and with unlimited number of votes on a planet

5. [OPTIONAL] Create a new modal window accessible from the main page where you display the statistics about voted planets.

    - There is a link in the header that opens a modal showing voting statistics based on the user votes saved in the database
    - The modal has an HTML `<table>` element containing the data
    - The columns of the table are `Planet name`, `Received votes`
    - Data is loaded into the table without page refresh (with AJAX)
    - There is an X icon in the top right corner and a `Close` button in the bottom right corner; clicking these closes the modal

6. [OPTIONAL] Do some improvements in order to make the web application easier to use.

    - Planet list is showing a loading indicator while the content is loading
    - Planet list navigation gets disabled while the requested data is loading
    - Residents modal is showing a loading indicator while the content is loading
    - Residents modal is not showing the table's header until the content is loaded
    - A nice background image is used, that fits nicely to the site and does not draw your attention out from actual content
    - Bootstrap is used with non-default colors is used (custom build, or a bootswatch theme)
