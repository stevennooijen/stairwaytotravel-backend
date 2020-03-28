# Mailchimp marketing logic

This document describes what logic has been build with regards to Mailchimp.
 
## Basics

* We work with one **audience** to keep all members in one place.
* A **signup form** is used for members to register to the audience. In our case, we fill in the form through the API.
* A form can have **hidden fields**, that a user doesn't see but we can use to fill in metadata about the user. For 
example, we included a field about page source that indicates whether someone signed up for the first time on the signup
 page or on the bucketlist page.
* For marketing **status** `'subscribed'`, one has to explicitly opt-in to receive e-mail marketing.
* That means that if someone provides his/her email for booking purposes on the 'bucketlist' page, he/she did not
give explicit **consent** for using the email address for marketing. Thus we set this member's status to`'transactional'` 
until he/she explicitly opts-in on the 'about' page.
* A marketing opt-in triggers an **automation** workflow that sends a welcome email to the newly subscribed member. 
This is called a **campaign**.
* Interaction with the campaign is automatically added to a member's **profile**. This stores every interaction of the 
member with our platform. Notes can be added to describe for example conversations you have had yourself.
* If emails bounce, Mailchimp automatically sets the member's status to `'cleaned'`. These can be ignored.
* To know what destinations someone has liked, we use member **events**. A custom event is created to add 'Liked 
destinations' to someone's profile. A member can have unlimited events and events can be used to trigger another 
automation to follow up on the requested booking.    

## Future work

* Create a booking event workflow.
* Add an opt-in possibility in the booking event workflow, so that more leads are converted into status `'subscribed'`.
* Create an opt-out possibility, so that members can `'unsubscribe'` from email marketing.
 
## Test scenarios

To test whether everything is configured properly, we kept the following journeys in mind:

### Scenario 1: book first, then opt-in for marketing

* Someone first completes the bucketlist booking flow
* If new, a member account will be created with status `'transactional'`
* Then a member event is created to store the liked destinations
* Later, the person signs up for email updates on the 'about' page
* The member already exists, so we need to update the status of the existing contact to `'subscribed'`

### Scenario 2: signup for marketing, then explore and book

* A person signs up on the 'about' page and gets status `'subscribed'`
* Someone then completes the bucketlist booking flow and fills in the form there
* The member already exists, so we only need to send a member event to keep track of the liked destinations
