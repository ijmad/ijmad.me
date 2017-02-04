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
  
  if request.path.startswith('/api/'):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
  else:
    response.cache_control.max_age = 3600
  
  return response


@app.route('/', methods=['GET'])
def index():
  return app.send_static_file('index.html')


@app.route('/robots.txt', methods=['GET'])
def robots():
  return app.send_static_file('robots.txt')


@app.route('/script/skype.js', methods=['GET'])
def script_skype():
  return Response(render_template('skype.js', SKYPE_NAME=os.environ['SKYPE_NAME']), mimetype='text/javascript')
  

@app.route('/script/captcha.js', methods=['GET'])
def script_captcha():
  return Response(render_template('captcha.js', RECAPTCHA_SITEKEY=os.environ['RECAPTCHA_SITEKEY']), mimetype='text/javascript')


@app.route('/api/email', methods=['POST'])
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
