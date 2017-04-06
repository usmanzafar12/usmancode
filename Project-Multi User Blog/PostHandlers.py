""" Module contains classes to handle Posts. This includes creating, editing
and deleting posts.
"""
import re
import time
from database import *
import query
import helper
import urllib
from hashlib import sha1
import logging


class ListPosts(helper.SecondaryHandler):
    def get(self):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        titles_list = query.get_all_posts(cookie_user, 'title', 'key')
        time.sleep(.5)
        return self.render("userblog.html", user=cookie_user.username_db,
                           text=titles_list.title, identifier=titles_list.key)


class CreatePost(helper.SecondaryHandler):
    def get(self):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        return self.render('blogentry.html')


class PostSuccess(helper.SecondaryHandler):
    def post(self):

        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')

        text = self.request.POST["blog"]
        title = self.request.POST["title"]
        identifier = self.request.POST["identifier"]
        if query.query_insert(cookie_user.username_db,
                              title, text, identifier):
            self.render("thanks.html", content=text)


class ViewPost(helper.SecondaryHandler):
    def get(self, doc_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        document = query.get_post(cookie_user, doc_id)
        comment_data = query.get_comments(doc_id, 'key', 'comment_content',
                                          'user')
        flag = self.set_like_flag(document, cookie_user)
        return self.render('post.html', method='post/blogentry',
                           title=document.title, content=document.post_text,
                           identifier=document.key.urlsafe(),
                           comments=comment_data.comment_content,
                           user=comment_data.user,
                           comment_identifier=comment_data.key,
                           count=len(document.likes), flag=flag)


class EditPost(helper.SecondaryHandler):
    def get(self, *args):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        doc_id = self.request.GET['name']
        document = query.get_post(cookie_user, doc_id)
        if document and cookie_user != document.user.get():
            return self.redirect('/error1')
        return self.render('blogentry.html', title=document.title,
                           content=document.post_text,
                           identifier=document.key.urlsafe())


class DeletePost(helper.SecondaryHandler):
    def get(self, post_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        document = query.get_post(cookie_user, post_id)
        if cookie_user != document.user.get():
            return self.redirect('/error1')
        query.delete_post(document.key.urlsafe())
        time.sleep(.5)
        self.redirect('/userblog')
