
# Hackathon APIs

A submissions app where one can see all the hackathons, register for the hackathon and can submit their hackathon submissions


## Context:
The hackathon can be posted by anyone and they will be authorized before they are allowed to post hackathons. Users should be able to come and submit some code or files as hackathon submissions. 


## Application Overview:
* Create hackathons by authorized users only with some basic fields
* Listing of hackathons
* Register to a hackathon
* Make Submissions
* Users will be able to list the hackathons they are enrolled to
* Users will be able to view their submissions in the hackathon they were enrolled in.

## Technologies/Framework/Libraries Used:

### Django
Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. Built by experienced developers, Django takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It is free and open source, has a thriving and active community, great documentation, and many options for free and paid-for support.

#### Why Django?
Django's comprehensive feature set, strong security, and established community make it a popular choice for building complex web applications. FastAPI and Flask, on the other hand, prioritize speed, flexibility, and simplicity. 

### REST API
A REST API is a popular way for systems to expose useful functions and data. REST, which stands for representational state transfer, can be made up of one or more resources that can be accessed at a given URL and returned in various formats, like JSON, images, HTML, and more.

### Django REST Framework
Django REST framework (DRF) is a powerful and flexible toolkit for building Web APIs. Reasone for using:
* The Web browsable API is a huge usability win.
* Authentication policies including packages for OAuth1a and OAuth2.
* Serialization that supports both ORM and non-ORM data sources.
* Customizable all the way down - just use regular function-based views if you don't need the more powerful features.

### Knox
Knox provides easy to use authentication for Django REST Framework The aim is to allow for common patterns in applications that are REST based, with little extra effort; and to ensure that connections remain secure. 
Knox authentication is token based, similar to the "TokenAuthentication" built in to DRF.

#### Why Knox
* DRF tokens are limited to one per user. This does not facilitate securely signing in from multiple devices, as the token is shared. It also requires all devices to be logged out if a server-side logout is required (i.e. the token is deleted).

* DRF tokens are stored unencrypted in the database. This would allow an attacker unrestricted access to an account with a token if the database were compromised.

* DRF tokens track their creation time, but have no inbuilt mechanism for tokens expiring. Knox tokens can have an expiry configured in the app settings (default is 10 hours.)



## API Reference

#### Register

```http
  POST /register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username`      | `string` | **Required**. Username for Register        |
| `password`      | `string` | **Required**. Pssword for Register        |
| `email`      | `string` | **Required**. Email for Register        |

#### Login

```http
  POST /login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Username for login        |
| `password`      | `string` | **Required**. Pssword for login        |

Output: TOKEN
####
Pass this token in Header of each API request as:
####
Authorization:  token {{TOKEN}}





#### Logout

```http
  POST /logout/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

#### List Hackathons

```http
  GET /hackathons/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


#### List a Particular Hackathons

```http
  GET /hackathons/<int:pk>/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the hackathon to retrieve      |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


#### Create a Hackathons

```http
  POST /hackathons/create/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `title`      | `string` | **Required**. The title of the hackathon      |
| `description`      | `string` | **Required**.  A description of the hackathon      |
| `background_image`      | `file` | **Required**. An image file to use as the background image for the hackathon      |
| `hackathon_image`      | `file` | **Required**. An image file to use as the hackathon image      |
| `type_of_submission`      | `string` | **Required**. The type of submission expected for the hackathon. Valid options are image, file, or link.     |
| `start_datetime`      | `datetime` | **Required**. The start date and time of the hackathon in ISO format (e.g. 2023-04-26T10:00:00Z).      |
| `end_datetime`      | `datetime` | **Required**. The start date and time of the hackathon in ISO format (e.g. 2023-04-26T10:00:00Z).     |
| `reward_prize`      | `decimal` | **Required**. The prize money to be awarded to the winners of the hackathon     |
| `Authorization`      | `string` | **Required**. A valid access token for an authenticated user.  |



#### Edit a Particular Hackathons

```http
  PUT /hackathons/<int:pk>/update/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the hackathon to retrieve      |
| `title`      | `string` | **Required**. The title of the hackathon      |
| `description`      | `string` | **Required**.  A description of the hackathon      |
| `background_image`      | `file` | **Required**. An image file to use as the background image for the hackathon      |
| `hackathon_image`      | `file` | **Required**. An image file to use as the hackathon image      |
| `type_of_submission`      | `string` | **Required**. The type of submission expected for the hackathon. Valid options are image, file, or link.     |
| `start_datetime`      | `datetime` | **Required**. The start date and time of the hackathon in ISO format (e.g. 2023-04-26T10:00:00Z).      |
| `end_datetime`      | `datetime` | **Required**. The start date and time of the hackathon in ISO format (e.g. 2023-04-26T10:00:00Z).     |
| `reward_prize`      | `decimal` | **Required**. The prize money to be awarded to the winners of the hackathon     |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |



#### Register to a Particular Hackathons

```http
  GET /hackathons/<int:pk>/register/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the hackathon to retrieve(Only which you have created)     |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

#### List all Registered Hackathons

```http
  GET /hackathons/registered/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |

#### Submit Submission for a Particular Hackathons

```http
  POST /hackathons/<int:pk>/submit/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the registered hackathon to retrieve      |
| `submission_name`      | `string` | **Required**. The name of your hackathon submission     |
| `submission_summary`      | `String` | **Required**. The summary for the hackathon submission     |
| `submission_image`      | `file` | **Required**. If the hackathon selected submission type is image      |
| `submission_link`      | `URL` | **Required**. If the hackathon selected submission type is link      |
| `submission_file`      | `file` | **Required**. If the hackathon selected submission type is file      |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |



#### View Submission for a Particular Hackathons

```http
  GET /hackathons/<int:pk>/submit/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `pk`      | `int` | **Required**. The ID of the registered hackathon to retrieve      |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


#### View All Submission for all hackathons

```http
  GET hackathons/listallsubmssions/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization`      | `string` | **Required**. The authentication token for the user making the request      |


## How to run

To downlaod this project

```bash
  git clone repo-link
```

Install all the dependencies 

```bash
  pip install -r requirements.txt
```

Make Migrations of the models

```python
  python manage.py makemigrations
```

Migrate Models to Database

```python
  python manage.py migrate
```

Runserver Locally

```python
  python manage.py runserver
```

