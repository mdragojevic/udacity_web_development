import webapp2
from main_page import BlogMainPage
from new_post import NewPost
from specific_entry import SpecificEntry
from registration import  RegistrationHandler
from welcome import WelcomeHandler
from login import LoginHandler
from logout import LogoutHandler
from blog_main_json import BlogMainJson
from spec_entry_json import SpecificJson
from handler import  Handler
from flush import FlushHandler

class MainHandler(Handler):
    def get(self):
        self.write('<h1><a href="/blog">Check out my blog!</a></h1>')

app = webapp2.WSGIApplication([
    ('/blog/?', BlogMainPage),
    ('/blog/.json', BlogMainJson),
    ('/blog/newpost', NewPost),
    ('/blog/(\d+)', SpecificEntry),
    ('/blog/(\d+).json', SpecificJson),
    ('/blog/signup', RegistrationHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler),
    ('/blog/welcome', WelcomeHandler),
    ('/', MainHandler),
    ('/blog/flush/?', FlushHandler)
], debug=True)
