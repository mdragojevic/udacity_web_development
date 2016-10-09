import webapp2
from main_page import BlogMainPage
from new_post import NewPost
from specific_entry import SpecificEntry
from registration import  RegistrationHandler
from welcome import WelcomeHandler
from login import LoginHandler
from logout import LogoutHandler
from handler import Handler

class MainHandler(Handler):
    def get(self):
        self.write('<h1><a href="/blog">Check out my blog!</a></h1>')

app = webapp2.WSGIApplication([
    ('/blog', BlogMainPage),
    ('/blog/newpost', NewPost),
    ('/blog/(\d+)', SpecificEntry),
    ('/blog/signup', RegistrationHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler),
    ('/blog/welcome', WelcomeHandler),
    ('/', MainHandler)
], debug=True)
