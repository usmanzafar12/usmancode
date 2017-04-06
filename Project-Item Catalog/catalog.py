""" This file serves as the main entry point for the app
    Code solves flask issue of static css files.
       Credit for code goes to Ostrovski:
    https://gist.github.com/Ostrovski/f16779933ceee3a9d181  """
from category import *
from item import *
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import OAuth2Credentials
import httplib2
import json
from flask import make_response
import requests
import logging
from apiclient import discovery
import os


app = Flask(__name__)
app.register_blueprint(bp_cat)
app.register_blueprint(bp_item)
flow = flow_from_clientsecrets('client_secrets.json', scope='openid',
                               redirect_uri='http://localhost:8000/auth')


@app.route('/login')
def login():
    """ This method serves as the entry point for oauth authentication """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # Using Google's client library to generate a request
    auth_uri = flow.step1_get_authorize_url(state=state)
    return redirect(auth_uri)


@app.route('/auth')
def code_exchange():
    if check_state():
        response = make_response("""There is a problem with
                                  your state, try again""")
        response.status_code = 401
        return response
    if check_error():
        response = make_response("""There is an error.
                                    You were not authorized, try again""")
        response.status_code = 401
        return response
    try:
        # Using Google's client library to exchange the auth code
        credentials = flow.step2_exchange(request.args.get('code'))
        login_session['credentials'] = credentials.to_json()
        return redirect('/verified')
    except FlowExchangeError:
        response = make_response('error in authentication')
        response.status_code = 401
        return response


@app.route('/verified')
def verified():
    credentials = login_session['credentials']
    cred_dict = json.loads(credentials)
    login_session['id'] = cred_dict['id_token']['sub']
    return redirect(login_session['path'])


@app.route('/logout')
def logout():
    login_session.pop('id', None)
    return redirect('/')


@app.route('/')
def main():
    session_check()
    cats = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('catalog.html', categories=cats,
                           login_session=login_session)


@app.route('/error<int:id>')
def error(id):
    if id == 1:
        resp = make_response("""<p>There seems to be an error
                                please try again<p>""")
        resp.status_code = 400
        return resp
    elif id == 2:
        resp = make_response("""<p>You are not authorized to do that<p>""")
        resp.status_code = 400
        return resp
    else:
        resp = make_response("""<p>There are items created by other users
                             in this category<p>""")
        resp.status_code = 400
        return resp


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def check_state():
    state = request.args.get('state', False)
    if login_session['state'] != state:
        return True
    else:
        return False


def check_error():
    if request.args.get('error', False):
        return True
    else:
        return False


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
