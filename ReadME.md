[![Build Status](https://travis-ci.org/joshtrigger/flask-api.svg?branch=develop)](https://travis-ci.org/joshtrigger/flask-api) 
[![Coverage Status](https://coveralls.io/repos/github/joshtrigger/flask-api/badge.svg?branch=develop)](https://coveralls.io/github/joshtrigger/flask-api?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/10e4a57f3b541a2c4da6/maintainability)](https://codeclimate.com/github/joshtrigger/flask-api/maintainability)

# Flask API
This API was solely developed in python using the python flask framework

## Requirements
    - Python
    - Text Editor e.g Vscode, SublimeText etc
    - Pytest

## Installation and setup
Run the following in your command line

    - pip install flask
    - pip install virtualenv
    - virtual venv
    - venv\Sripts\activate 
    - pip install Flask-RESTful

To deactivate the virtual enviroment run `deactivate`

## Testing
Testing of the API was done using postman, you can get it [here](https://www.getpostman.com/) 

## Hosting API on heroku
First and foremost, ensure that your github repository is connected to heroku. Then add the required files that will enable heroku host your application. Now you can safely deploy your API to heroku. Check out mine [here](https://my-fast-food-api.herokuapp.com)

## Documentating the API
API documentation is a concise manual containing all the information required to work with the API. It contains instructions on how to effectively use the API. I documented my API using swagger, check it out [here](https://my-fast-food-api.herokuapp.com/apidocs/)

## API endpoints for the application
Request|URL|Description
---|---|---
**POST**|`/auth/signup`|Register User
**POST**|`/auth/login`|Login User
**GET**|`/orders`|Get all orders
**GET**|`/orders/orderId`|Fetch a specific order by its ID
**POST**|`/users/orders`|Place new order
**GET**|`/users/orders`|Order history
**PUT**|`/orders/orderId`|Update order status
**DELETE**|`/orders/orderId`|Delete an order
**GET**|`/menu`|Get available menu
**POST**|`/menu`|Add a meal
**DELETE**|`/menu/foodId`|Delete an item on menu