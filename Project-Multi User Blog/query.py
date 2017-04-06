from google.appengine.ext import ndb
import logging
from database import *


class DataObject:
    """ this class stores attributes of all data classes  """
    def __init__(self, titles=[], posts=[], username=[], salted_password=[],
                 key=[], content=[], user=[]):
        self.title = titles
        self.post_text = posts
        self.username_db = username
        self.salted_password_db = salted_password
        self.key = key
        self.comment_content = content
        self.user = user


def get_post(user, doc_id):
    """this function retrieves the post with the given ID"""
    post = ndb.Key(urlsafe=doc_id).get()
    if post:
        return post
    else:
        return False


def get_posts(obj_user, *a):
    """this function retrieves all posts associated with a given username"""
    data = DataObject()
    temp = obj_user.posts_db  # get related posts of User object
    for var in a:
        dummy = []
        for val in temp:  # get related attributes of Posts object
            if var == 'key':
                dummy.append(val.get().key.urlsafe())
            else:
                dummy.append(getattr(val.get(), var))
        setattr(data, var, dummy)
    return data


def get_all_posts(user, *a):
    """function retrieves all the posts from the datastore"""
    data = DataObject()
    posts = Post.query().fetch()
    for var in a:
        dummy = []
        for val in posts:  # get related attributes of Posts object
            if var == 'key':
                dummy.append(val.key.urlsafe())
            else:
                dummy.append(getattr(val, var))
        setattr(data, var, dummy)
    return data


def query_insert(user, text, content, identifier=None):
    """this function inserts a post into the datastore"""
    obj_user = get_user(user)
    flag = post_check(identifier)
    if flag:
        post = flag
        post.title = text
        post.post_text = content
        post.user = obj_user.key
        post.put()
    else:
        post = Post(title=text, post_text=content, user=obj_user.key)
        post.put()
    insert_post_key(obj_user, post)
    return True


def post_check(post_id=None):
    # this function checks if the post already existed
    if post_id:
        obj = ndb.Key(urlsafe=post_id).get()
    else:
        obj = False
    if obj:
        return obj
    else:
        return False


def insert_post_key(user, post):
    """ this function helps query_insert with inserting a post """
    if post.key not in user.posts_db:
        user.posts_db.append(post.key)
        user.put()
    else:
        pass


def cookie_get_user(hash_value):
    """ this function gets the User object associated with a cookie """
    q = "SELECT * FROM Cookie WHERE cookie_value = '"+hash_value+"'"
    obj_cookie = ndb.gql(q).get()
    if obj_cookie:
        obj_user = obj_cookie.user.get()
        return obj_user
    else:
        return False


def cookie_del_user(cookie_user):
    """ this function deletes a cookie from the datastore """
    q = "SELECT * FROM Cookie WHERE user =" + str(cookie_user.key)+""
    obj_cookie = ndb.gql(q).get()
    return obj_cookie.key.delete()


def get_user(username):
    """ this function returns the User object of a given username  """
    q = "SELECT * FROM User WHERE username_db = '"+username+"'"
    obj = ndb.gql(q).get()
    return obj


def delete_post(key_value):
    """ this function deletes a post by its key_value """
    post_key = ndb.Key(urlsafe=key_value)
    post_key.delete()


def insert_comment(obj_user, obj_post, content):
    """ this function inserts a comment to a post """
    comment = Comments(comment_content=content, user=obj_user.key,
                       post=obj_post.key)
    comment_key = comment.put()
    obj_post.comments.append(comment_key)
    obj_post.put()


def get_comments(post_id, *a):
    """this function retrives all the comments related to a post"""
    data = DataObject()
    obj_post = ndb.Key(urlsafe=post_id).get()
    temp = obj_post.comments
    if temp:
        for var in a:
            dummy = []
            for val in temp:
                if var == 'key':
                    dummy.append(val.urlsafe())
                elif var == 'user':
                    dummy.append(val.get().user.get().username_db)
                else:
                    dummy.append(getattr(val.get(), var))
            setattr(data, var, dummy)
    return data


def get_comment(key_url):
    """function gets a specific comment from the specifed key"""
    comment_key = ndb.Key(urlsafe=key_url)
    return comment_key.get()


def edit_comment(obj_comment, content):
    """this function edits the given comment object"""
    obj_comment.comment_content = content
    obj_comment.put()


def delete_comment(obj_comment):
    """this function deletes the comment from the datastore"""
    obj_post = obj_comment.post.get()
    obj_post.comments.remove(obj_comment.key)
    obj_post.put()
    obj_comment.key.delete()


def add_like(cookie_user, obj_post):
    """this function adds a like to the post object"""
    if cookie_user.key not in obj_post.likes:
        obj_post.likes.append(cookie_user.key)
        return obj_post.put()
    else:
        return False


def delete_like(cookie_user, obj_post):
    """this function deletes a like to the post object"""
    if cookie_user.key in obj_post.likes:
        obj_post.likes.remove(cookie_user.key)
        return obj_post.put()
    else:
        return False


def query_helper(query, *a):
    """ this is a generic query function that can
        return the passed attributes """
    data = DataObject
    q = ndb.gql(query)
    for index, value in enumerate(a):
        dummy = []
        for obj in q.fetch(limit=None):
            dummy.append(getattr(obj, a[index]))
        setattr(data, a[index], dummy)
    return data
