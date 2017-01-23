#!/usr/bin/env python

import os, requests
from flask import Flask, Response, render_template, request, redirect, jsonify, abort


app = Flask(__name__, static_url_path='/static')

@app.before_request
def check_secure():
  bearer_found = request.headers.get('Authorization', None)
  bearer_required = os.environ.get('BEARER_AUTH', None)
  if bearer_required and (('Bearer ' + bearer_required) != bearer_found):
    abort(403)
  
  proto = request.headers.get('X-Forwarded-Proto', None)
  if proto == 'http':
    return redirect(request.url.replace('http://', 'https://'), 301)


@app.after_request
def add_headers(response):
  response.headers["Strict-Transport-Security"] = "max-age=86400; includeSubDomains"
  
  if request.path == '/' or request.path.startswith('/static'):
    response.cache_control.max_age = 3600
  else:
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
  
  return response


@app.route('/', methods=['GET'])
def index():
  return app.send_static_file('index.html')


@app.route('/captcha.js', methods=['GET'])
def captcha():
  return Response(render_template('captcha.js', RECAPTCHA_SITEKEY=os.environ['RECAPTCHA_SITEKEY']), mimetype='text/javascript')


@app.route('/email', methods=['POST'])
def email():
  params = {
    'remoteip': request.remote_addr,
    'secret': os.environ['RECAPTCHA_SECRET'],
    'response': request.form.get('g-recaptcha-response')
  }

  verify_response = requests.get(os.environ['RECAPTCHA_URL'], params=params, verify=True)
  if verify_response.json()['success']:
    return jsonify(email=os.environ['EMAIL_ADDRESS'])
  else:
    abort(403)
    

if __name__ == '__main__':
  port = int(os.environ.get('PORT',5000))
  app.run(host='0.0.0.0', port=port, debug=True)
