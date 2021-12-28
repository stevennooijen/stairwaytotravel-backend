# Mailchimp marketing logic

This document describes what logic has been build with regards to Mailchimp.

## Basics

* We work with one **audience** to keep all members in one place.
* A **signup form** is used for members to register to the audience. In our case, we fill in the form through the API.
* A form can have **hidden fields**, that a user doesn't see but we can use to fill in metadata about the user. For
example, we included a field about page source that indicates whether someone signed up for the first time on the signup
 page or on the bucketlist page.
* Mailchimp uses the **status** field to indicate whether someone has opted-in for marketing. `'subscribed'` means
someone did. Other statuses are `transactional` and `unsubscribed`. Opt-in can be done through single or double opt-in.
* Status `transactional` means that someone can only receive transactional email. This would be for example an order
notification. Sadly, Mailchimp does not allow transactional email based on events (which is our case). This would have
been our preferred scenario as the bucket list confirmation email could be considered a 'transaction'.
* That means we need to set everybody to status `subscribed` in order to email them their bucket list confirmation, and
keep a separate field for administrating if someone opts-in for mass email marketing.
* So, if someone provides his/her email for booking purposes on the 'bucketlist' page, he/she did not
give explicit **consent** for using the email address for marketing. Thus we set this member's `MARKETING` merge field
to 'no' until he/she explicitly opts-in on the 'about' page.
* A marketing opt-in triggers an **automation** workflow that sends a welcome email to the newly subscribed member.
This is called a **campaign**.
* Interaction with the campaign is automatically added to a member's **profile**. This stores every interaction of the
member with our platform. Notes can be added to describe for example conversations you have had yourself.
* If emails bounce, Mailchimp automatically sets the member's status to `'cleaned'`. These can be ignored.
* To know what destinations someone has liked, we use member **events**. A custom event is created to add 'Liked
destinations' to someone's profile. A member can have unlimited events and events can be used to trigger another
automation to follow up on the requested booking.

## Stored information

We store information from the booking process at two levels:
1. In the **merge fields** that are defined at the user level. We keep track of:
    * `status`: needs to be `subscribed` to be able to email them at all.
    * `marketing`: a radio button that indicates whether someone opted-in for mass email.
    * `location`: the url path from where the user first signed up.
    * `util_html`: an 'utility' or helper field that we use to temporarily store html that we generate for the bucket
    list confirmation email. This is a bit of a hack: it would have been prettier if Mailchimp would allow us to read
    in the liked destination list from a member event instead of from a user's profile (see Trello card with issues on
    this topic).
    * `booking_type`: checkboxes that indicates what type of booking support a user has opted-in for at
    their *last* event.
    * `boooking_interest`: a radio button that indicates whether the user opted-in for booking support at
    their *last* event.
2. Through **member events**. A user has one event for each time he/she submits the booking form.
    * `likes_ids`: a list of the liked destination ids.
    * `likes_titles`: a list of the liked destination titles, for easier readability.
    * `booking_type`: checkboxes that indicates what type of booking support a user has opted-in for.

## API workflow

When submitting a bucket list flow, the following sequence of emails is kicked-off:
1. A **post** request to create a user (signup). This includes all fields mentioned under `merge_fields` above.
If the user already exists, this returns `null`.
2. In case the user already exists (a `null` response), a **patch** request is made to update the user's `merge_fields`
information.
3. A **post** request to add a member event with the member event fields mentioned above.

## Future work

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
