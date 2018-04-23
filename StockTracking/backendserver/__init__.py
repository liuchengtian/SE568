#!/usr/bin/env python
# -*- coding: utf-8 -*-

#init
from flask import Flask
# from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Bootstrap(app)

<<<<<<< HEAD
from StockTracking.backendserver.controller import app

=======
from StockTracking.backendserver.controller import controller
from StockTracking.backendserver import data
from StockTracking.backendserver import rss
>>>>>>> 76ddb4d6b6709659ee981672df9264bc6615a273
