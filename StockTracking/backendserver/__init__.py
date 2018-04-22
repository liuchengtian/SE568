#!/usr/bin/env python
# -*- coding: utf-8 -*-

#init
from flask import Flask
# from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Bootstrap(app)

from StockTracking.backendserver.controller import controller

