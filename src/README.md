## Requirements:
* pip3 install flask
* pip3 install flask_cors\
\
Tested on Python 3.6.9, might work on 2.7 but haven't tested it


## To run:
Currently the introNode server doesn't do much other than forward the JSON message to the final server, but it's used to simply give a basic idea of the process the message will go through.

* On one terminal run 'python3 server.py'
* On another terminal run 'python3 introNode.py'
* In your browser, enter 'localhost:5000/'

To run without starting the currently unnecessary introNode, just change the port number in line 50 of 'src/templates/layout.html' from 10000 to 5000. Then to run simply do:

* In a terminal run 'python3 server.py'
* In your browser, enter 'localhost:5000/'
