from CommentHandlers import *


class MainPage(helper.SecondaryHandler):
    def get(self):
        self.render("main.html")


class Error(helper.SecondaryHandler):
    def get(self, error_id):
        if str(error_id) == '1':
            self.render('error.html', message="""You are
                        unauthorised to do that""")
        elif str(error_id) == '2':
            self.render('error.html', message="""You cannot
                        like your own post pence chor""")
        elif str(error_id) == '3':
            self.render('error.html', message="""You cannot unlike
                        your own post pence chor""")


class LikePost(helper.SecondaryHandler):
    def get(self, post_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        obj_post = query.get_post(cookie_user, post_id)
        if cookie_user.key == obj_post.user:
            return self.redirect('/error2')
        query.add_like(cookie_user, obj_post)
        return self.redirect('/post-'+str(post_id))


class UnlikePost(helper.SecondaryHandler):
    def get(self, post_id):
        cookie_user = self.cookie_check()
        if not cookie_user:
            return self.redirect('/sin')
        obj_post = query.get_post(cookie_user, post_id)
        if cookie_user.key == obj_post.user:
            return self.redirect('/error3')
        query.delete_like(cookie_user, obj_post)
        return self.redirect('/post-'+str(post_id))


app = helper.webapp2.WSGIApplication([
    ('^/', MainPage),
    ('^/sin|/sin/userblog', Login),
    ('^/blogentry', CreatePost),
    ('^/post/thanks|/thanks', PostSuccess),
    ('^/register$|^/regcheck$', Register),
    ('^/userblog', ListPosts),
    ('^/logout', LogOut),
    ('^/post-(.*)', ViewPost),
    ('^/post/blogentry(.*)', EditPost),
    ('^/error(.*)', Error),
    ('^/delete-(.*)', DeletePost),
    ('^/addcomment-(.*)', AddComment),
    ('^/editcomment-(.*)', EditComment),
    ('^/delcomment-(.*)', DeleteComment),
    ('^/like-(.*)', LikePost),
    ('^/unlike-(.*)', UnlikePost)
], debug=True)
