# import dependencies
from flask import Flask



# Create a Flask instance called app
app = Flask(__name__)



# Create first route which is the root
@app.route('/')
# Create function hello_world()
def hello_world():
    return 'Hello World'

