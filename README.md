# FSND Capstone Project: Casting Agency API

**APPLICATION ROOTS**: 

- Production App Root:

```txt
https://gs-sample-deploy.herokuapp.com/
```

- Local Development App Root:

```shell
http://127.0.0.1:5000/
```



## Getting Started

---

### Installing Dependencies:

**Python 3.7**

Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

**Virtual Environment**

It is recommended to utilize a virtual environment to run this project locally. This will allow us to ensure that your project can wrap it's particular set of dependencies to the project scope, and ensures you're not polluting the global python installation on your local machine. Complete instructions for setting up a proper virtual environment can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

> **Virtual Environment Quick Start**
>
> ```shell
> python3 -m venv venv
> ```
>
> ```shell
> source venv/bin/activate
> ```
>
> - check if the right version has been sourced:
>
> ```shell
> which python
> which python3
> ```
>
> - deactivate virtual environment
>
> ```shell
> deactivate
> ```



**Install Dependencies**

```shell
pip install -r requirements.txt
```

- This will install all of the required packages we defined in `requirements.txt`.



## Setup Databases

### Setup Primary Database

```shell
createdb casting
```

- Setup environment variable to hold primary database path:

```shell
export DATABASE_URL=<URI_TO_DATABASE> 
```

> **NOTE**: For easy operation, you can reset and seed the local database by [clicking here](http://127.0.0.1:5000/api/seed) or navigating to:
>
> http://127.0.0.1:5000/api/seed
>
> This will generate the initial data needed for the application, and will reset the database if data has already been seeded. 
>
> **ALSO NOTE**: you do not need to be authenticated to trigger this endpoint



### Setup Testing Database

```shell
createdb casting_test
```

- Setup environment variable to hold primary database path:

```shell
export TEST_DATABASE_URL=<URI_TO_DATABASE> 
```

> Any tests being run will get executed by default against this secondary database. And can be accessed by registered collaborators at: https://dashboard.heroku.com/apps/gs-sample-deploy/settings



**Running Tests**

> Run tests against local testing database:
>
> ```shell
> python test_api.py
> ```
>
> **NOTE**: `TEST_DATABASE_URL` must be set locally. See[ `Setup Local Testing Database`](#setup-testing-database)
>
> 
>
> Run tests against production testing database:
>
> ```shell
> python test_prod_api.py
> ```
>
> **NOTE**: production testing database is already configured with the necessary environment variables 





**Running The Server**

```shell
# Automatically set environment configuration:
source setup.sh
```

> If you prefer to manually set and configure your local environment the following variables will need to be defined:
>
> - `AUTH0_DOMAIN``
> - `AUTH0_ALGORITHMS`
> - `AUTH0_AUDIENCE`
>
> Currently for review purposes the following tokens are also set via environment variables, and provided in the `setup.sh` configuration:
>
> - `EXEC_PROD_TOKEN` - has access to all endpoints and functions
> - `CAST_DIR_TOKEN` - has limited access to most endpoints and functions
> - `CAST_ASST_TOKEN` - has extremely limited access and only basic view functions for each endpoint
>
> Additional environment variables that **MUST BE SET** based on your local database configuration:
>
> - `DATABASE_URL` - used to define your local database path
> - `TEST_DATABASE_URL` - used to define your local test database path
>
> **NOTE:** The neccessary <u>database paths are already configured via Heroku's production environment</u>
>
> 
>
> You can also manually set the following if they differ for your purposes:
>
> ```shell
> # set default app entry-point:
> export FLASK_APP=app.py
> # set development mode to monitor and refresh app on file changes:
> export FLASKENV=development
> ```
>
> - Runs the Flask server :
>
> ```shell
> # used to fire up the server:
> flask run --reload
> ```





## API Reference

---

| API Base URL:                              | Environment:               |
| ------------------------------------------ | -------------------------- |
| https://gs-sample-deploy.herokuapp.com/api | Production API Base URL    |
| http://127.0.0.1:5000/api                  | Local Development Base URL |



### All Available Endpoints:

| Endpoint:            | Available Methods:     | Details:                                                     |
| -------------------- | ---------------------- | ------------------------------------------------------------ |
| `/`                  | `GET`                  | returns the application index route                          |
| `/actors`            | [`GET, POST`]          | used to `GET` a `list` of all `actors` and `POST` new `actors` |
| `/movies`            | [`GET, POST`]          | used to `GET` a `list` of all `movies` and `POST` new `movies` |
| `/actors/<actor_id>` | [`GET, PATCH, DELETE`] | used to `GET` a single `actor` by `actor_id`, or `PATCH`  a single `actor` by `actor_id` or `DELETE` a single `actor` by `actor_id` |
| `/movies/<movie_id>` | [`GET, PATCH, DELETE`] | used to `GET` a single `movie` by `movie_id`, or `PATCH`  a single `movie` by `movie_id` or `DELETE` a single `movie` by `movie_id` |



### Permissions By Role:

| Permissions     | Roles                                                       | Details                                                      |
| --------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| `get:actors`    | [`executive_producer, casting_director, casting_assistant`] | provides a list of all actors or a single actor, using the `actor_id` as a url param |
| `get:movies`    | [`executive_producer, casting_director, casting_assistant`] | provides a list of all movies or a single movie, using the `movie_id` as a url param |
| `post:actors`   | [`executive_producer, casting_director`]                    | allows user to create a new actor, using the `POST` method   |
| `post:movies`   | [`executive_producer`]                                      | allows user to create a new movie, using the `POST` method   |
| `patch:actors`  | [`executive_producer, casting_director`]                    | allows user to update a new actor, using the `PATCH` method  |
| `patch:movies`  | [`executive_producer, casting_director`]                    | allows user to update a new movie, using the `PATCH` method  |
| `delete:actors` | [`executive_producer, casting_director`]                    | allows user to update a new actor, using the `DELETE` method |
| `delete:movies` | [`executive_producer`]                                      | allows user to update a new movie, using the `DELETE` method |



## Endpoint Usage

**`GET /actors`**

> - Fetch a list of `actors`
> - Args: `none`
> - Returns: `JSON` containing all info related to each actor
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actors": [
>     {
>       "age": 25,
>       "gender": "m",
>       "id": 1,
>       "name": "Sam Jones"
>     },
>     {
>       "age": 22,
>       "gender": "f",
>       "id": 2,
>       "name": "Cynthia Jones"
>     },
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 3,
>       "name": "Vanna White"
>     }
>   ],
>   "success": true
> }
> ```



**`GET /movies`**

> - Fetch a list of `movies`
> - Args: `none`
> - Returns: `JSON` containing all info related to each movie
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 1,
>       "title": "The Movie",
>       "year": 2015
>     },
>     {
>       "id": 2,
>       "title": "The Movie 2",
>       "year": 2016
>     },
>     {
>       "id": 3,
>       "title": "The Movie 3",
>       "year": 2017
>     }
>   ],
>   "success": true
> }
> ```



**`GET /actors/<int:actor_id>`**

> - Fetch a single `actor` by `actor_id`
> - Args: `none`
> - Returns: `JSON` containing all info related to each actor
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actor": {
>     "age": 22,
>     "gender": "f",
>     "id": 2,
>     "name": "Cynthia Jones"
>   },
>   "success": true
> }
> ```



**`GET /movies/<int:movie_id>`**

> - Fetch a single `movie` by `move_id`
> - Args: `none`
> - Returns: `JSON` containing all info related to each movie
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movie": {
>     "id": 2,
>     "title": "The Movie 2",
>     "year": 2016
>   },
>   "success": true
> }
> ```





**`POST /actors`**

> - Insert new actor record into database
> - Args: `name, age, gender`
> - Returns: `JSON` reponse containing request status, and new actor details
>
> **EXAMPLE RESPONSE**
>
> ```json
> {
>   "actor": {
>     "age": 24,
>     "gender": "m",
>     "id": 4,
>     "name": "Tim Adams"
>   },
>   "success": true
> }
> ```





**`POST /movies`**

> - Insert new movie record into database
> - Args: `title, year`
> - Returns: `JSON` response containing request status and new movie details
>
> **EXAMPLE RESPONSE**
>
> ```json
> {
>   "movie": {
>     "id": 4,
>     "title": "The Movie 4",
>     "year": 2017
>   },
>   "success": true
> }
> ```



**`PATCH /actors/<int:actor_id>`**

> - Fetch a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` repsonse containing request status and updated actor details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "actors": [
>     {
>       "age": 32,
>       "gender": "f",
>       "id": 2,
>       "name": "Samantha Adams"
>     }
>   ],
>   "success": true
> }
> ```
>
> 



**`PATCH /movies/<int:movie_id>`**

> - Fetch a single `movie` by `movie_id`
> - Args: `movie_id`
> - Returns: `JSON` repsonse containing request status and updated movie details
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "movies": [
>     {
>       "id": 2,
>       "title": "The Movie 4.1",
>       "year": 2018
>     }
>   ],
>   "success": true
> }
> ```



**`DELETE /actors/<int:actor_id>`**

> - Delete a single `actor` by `actor_id`
> - Args: `actor_id`
> - Returns: `JSON` repsonse containing request status and deleted `actor_id`
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "delete": 4,
>   "success": true
> }
> ```



**`DELETE /movies/<int:movie_id>`**

> - Delete a single `movie` by `movie_id`
> - Args: `movie_id`
> - Returns: `JSON` repsonse containing request status, and deleted `movie_id`
>
> **EXAMPLE RESPONSE:**
>
> ```json
> {
>   "delete": 4,
>   "success": true
> }
> ```

