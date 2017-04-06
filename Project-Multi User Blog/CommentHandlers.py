"""Module contains functions for handling comments. This includes
creating, updating, deleting comments
"""
from AuthenticationHandlers import *


class AddComment(helper.SecondaryHandler):
    def post(self, post_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        comment_body = self.request.get('comment', False)
        post = query.get_post(cookie_user, post_id)
        query.insert_comment(cookie_user, post, comment_body)
        self.redirect('/post-'+str(post_id))


class DeleteComment(helper.SecondaryHandler):
    def get(self, comment_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        obj_comment = query.get_comment(comment_id)
        if obj_comment.user != cookie_user.key:
            return self.redirect('/error1')
        query.delete_comment(obj_comment)
        time.sleep(.5)
        return self.redirect('/post-'+str(obj_comment.post.urlsafe()))


class EditComment(helper.SecondaryHandler):
    def get(self, comment_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        obj_comment = query.get_comment(comment_id)
        if obj_comment.user != cookie_user.key:
            return self.redirect('/error1')
        else:
            self.render('editcomment.html',
                        content=obj_comment.comment_content,
                        identifier=obj_comment.key.urlsafe())

    def post(self, comment_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        content = self.request.get('comment')
        obj_comment = query.get_comment(comment_id)
        # Making sure that only the current user can edit.
        if obj_comment.user != cookie_user.key:
            return self.redirect('/error1')
        query.edit_comment(obj_comment, content)
        self.redirect('/post-'+obj_comment.post.urlsafe())
