from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

config = {
    "CACHE_TYPE": "SimpleCache", 
}

app = Flask(__name__)
app.config.from_mapping(config)
CORS(app)
cache = Cache(app)

import local_data

import api

app.run("0.0.0.0")