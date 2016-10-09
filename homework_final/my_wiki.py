import webapp2
from registration import  RegistrationHandler
from login import LoginHandler
from logout import LogoutHandler
from handler import  Handler
from wiki_handler import WikiHandler
from edit_handler import EditHandler
from history import HistoryHandler

class MainHandler(Handler):
    def get(self):
        self.write('<h1><a href="/blog">Check out my blog!</a></h1>')

DEBUG = True
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([('/signup', RegistrationHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),
                               ('/_edit' + PAGE_RE, EditHandler),
                               ('/_history' + PAGE_RE, HistoryHandler),
                               (PAGE_RE, WikiHandler),
                               ],
                              debug=DEBUG)
