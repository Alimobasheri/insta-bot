# InstaBot API.

This API is implemented using Python and Flask to handle collaboation with the scraper. The API stores and manages the fake user, the target users and calls the scraper for updating the target users' feed by each request to the /update endpoint. Each target users' feed can be accessed by calling the get-feed endpoint.

### API Map:

#### GET /api/insta/set-fakeuser?username=xxx&password=yyyyy HTTP 1.1
##### Description: 
Updates the fake user account which is used to login to Instagram.
##### Parameters: 
1. username: The new username.
2. password: the new password.

#### GET /api/insta/get-fakeuser
##### Description:
Returns the current fake user's username. The password is not returned due to security reasons.
