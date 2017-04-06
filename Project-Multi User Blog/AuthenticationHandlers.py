"""Module contains classes for handling registeration and authentication.
 This includes log in, log out and register
"""
from PostHandlers import *


class LogOut(helper.SecondaryHandler):
    def get(self):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        else:
            temp = query.cookie_del_user(cookie_user)
            return self.redirect('/')


class Login(helper.SecondaryHandler):
    def get(self):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.render("sign-in.html")
        else:
            return self.redirect('/userblog')

    def post(self):
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        if self.authenticate(username, password):
            cookie_user = query.cookie_get_user(
                                             self.calc_cookie_hash(username))
            obj_user = query.get_user(username)
            if not cookie_user:
                temp = self.create_cookie(self.calc_cookie_hash(username),
                                          obj_user)
            self.response.set_cookie('user_id',
                                     self.calc_cookie_hash(username), path='/')
            self.redirect("/userblog")
            return time.sleep(.5)
        else:
            self.redirect('/sin')
            return self.render("sign-in.html", error_message="""The username
                                or password is incorrect""")


class Register(helper.SecondaryHandler):
    def get(self):
        self.render("register.html", name="", message="")

    def post(self):
        username = self.request.POST["username"]
        password = self.request.POST["password"]
        bool_user = self.validate_string(username)
        bool_pwd = self.validate_string(password)
        if not bool_user or not bool_pwd:
            return self.render("register.html", name=username, message=""" The
                               username or password
                               is not correct. Please enter any
                               alphanumeric character
                               with a length between 4 and 10 characters
                               """)
        obj_user = self.username_check(username)
        if not obj_user:
            obj_user = self.register_user(username, password)
            temp = self.create_cookie(self.calc_cookie_hash(username),
                                      obj_user)
            self.response.set_cookie('user_id',
                                     self.calc_cookie_hash(username), path='/')
            time.sleep(.5)
            self.redirect('/userblog')
        else:
            self.render('register.html', name=username,
                        message="""This username has been taken.
                                   please enter another one""")
