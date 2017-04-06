from google.appengine.ext import ndb
import jinja2
import os
import logging
from hashlib import sha1
import query
import webapp2
from database import *
import re


html_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(html_dir),
                               autoescape=True)


class SecondaryHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        """ the funcintion prints out the http response """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ this function renders the template by using jinja """
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def calc_cookie_hash(self, username):
        """ this function calculates the hash value of a username string """
        value = 'random' + username
        return sha1(value).hexdigest()

    def create_cookie(self, val, cookie_user):
        """ this function stores the cookie value and the associated user """
        cookie = Cookie(cookie_value=val, user=cookie_user.key)
        logging.error(cookie)
        return cookie.put()

    def username_check(self, username):
        """ this function checks the username if it exists in the database """
        q = """ SELECT * FROM User WHERE username_db = '"""+username+"""' """
        # returns userobject or null
        check_user = query.query_helper(q, 'username_db')
        if check_user.username_db:
            return check_user
        else:
            return False

    def password_check(self, salted_password):
        """ this functions checks if the password is correct """
        salt = "usman"
        salted_password = sha1(salt + salted_password).hexdigest()
        q = """ SELECT * FROM User WHERE
        salted_password_db = '""" + salted_password + "'"
        check_password = query.query_helper(q, 'salted_password_db')
        if check_password.salted_password_db:
            return check_password
        else:
            return False

    def cookie_check(self):
        cookie = self.request.cookies.get('user_id', False)
        if not cookie:
            cookie_user = False
        else:
            cookie_user = query.cookie_get_user(cookie)
        if not cookie_user:  # implies that the cookie id does not exist in db
            return False
        else:
            return cookie_user

    def authenticate(self, username, password):
        """ authenticates if a username and password is
            correct for registered users """
        user_check = self.username_check(username)
        password_check = self.password_check(password)
        if user_check and password_check:
            return True
        else:
            return False

    def validate_string(self, string):
        """Method validates a string according to the regex """
        # length between 4 and  6 characters
        regex = "\A(?=\w{4,10}\Z)"
        if re.search(regex, string):
            return True
        else:
            return False

    def register_user(self, username, password):
        """ Method registers a user."""
        salt = "usman"
        salted_password = sha1(salt+password).hexdigest()
        user = User(username_db=username, salted_password_db=salted_password)
        user.put()
        return user

    def set_like_flag(self, obj_post, cookie_user):
        if cookie_user.key in obj_post.likes:
            return False
        else:
            return True
