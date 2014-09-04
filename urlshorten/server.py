#!/usr/bin/env pythone

"""

Author: Rajneesh Mitharwal: Created at 04 september 2014

"""
from flask import (Flask, request,redirect, abort,jsonify,make_response)

from utils.config import Config
from utils.dbconnections import DbConnections
from utils.analytics.analyticslog import FileLogger

import logging
import shorten
import time
import json

app = Flask(__name__)

config_obj = Config()
app.shorten_config = Config().dataMap
app.dbconnections=DbConnections.fromConfig(config_obj)

def add_analytics_log(long_url,short_url,method):
    """
    log event for analytics
    """
    data = dict(short_url_len=len(short_url),long_url_len=len(long_url),requested_at= int(time.time()))
    FileLogger.info(method, json.dumps(data))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request', 'pass': "false"} ), 400)

@app.route('/<path:short_url>', methods = ['GET'])
def redirect_short_url(short_url):   
    if not short_url:
        abort(400)
    url_shorten = shorten.UrlShortener(app.dbconnections)
    long_url = url_shorten.get_long_url(short_url)
    if not long_url:
        return not_found("not seen this short url before")
    add_analytics_log(long_url,short_url,method="get")
    return redirect(long_url, code=302)

@app.route('/', methods = ['POST'])
def generate_short_url():
    long_url = request.form.keys()[0]
    if not long_url:
        abort(400)
    url_shorten = shorten.UrlShortener(app.dbconnections)
    short_url = url_shorten.get_short_url(long_url)
    add_analytics_log(long_url,short_url,method="post")
    status = "true" if short_url else "false"  
    return jsonify( { 'pass': status, 'url': short_url } ), 201

if __name__ == '__main__':
    logging.error("Starting url shorten server.....")
    app.run(debug = True)     