# Spin the Wheel of Fortune

Write description here!


## Code stuff

We have two components: backend and frontend. 

Flask:
- https://flask.palletsprojects.com/en/2.1.x/
- So this will be the server that runs all the qiskit stuff.
- The plan is the front end will call it for all queries. e.g. when a player does a measurement


### Setup
Consider setting up a python virtual environment, for python 3.7 or greater.

Install Flask:
pip install flask

To run server:
(in the wheel-of-fortune-game folder)
flask run

Now install web server.
Mac: brew install npm
Linux: sudo apt install npm

npm install --global http-server

Go to directory, and run http-server.

#### Access-Control-Allow-Origin
(Actually you probably don't need this any more)
To get around this security issue, use chrome, and install 
this plugin:
https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf

