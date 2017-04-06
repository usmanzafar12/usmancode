from google.appengine.ext import ndb


class Post(ndb.Model):
    """Post Class stores attributes related to posts"""
    title = ndb.StringProperty(required=True)
    post_text = ndb.TextProperty(required=True)
    user = ndb.KeyProperty()
    comments = ndb.KeyProperty(repeated=True)
    likes = ndb.KeyProperty(repeated=True)


class User(ndb.Model):
    """User class stores attributes related to User"""
    username_db = ndb.StringProperty(required=True)
    posts_db = ndb.KeyProperty(kind=Post, repeated=True)
    salted_password_db = ndb.StringProperty(required=True)


class Cookie(ndb.Model):
    """Cookie class stores attributes related to Cookie"""
    cookie_value = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(kind=User)


class Comments(ndb.Model):
    """Comments class stores attributes related to Comments"""
    comment_content = ndb.TextProperty()
    user = ndb.KeyProperty()
    post = ndb.KeyProperty()
