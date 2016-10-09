from handler import Handler
from db_models import User
import cgi
import re
from google.appengine.ext import db
import encoding as enc
from user_input_validation import validate_username, validate_password



class LogoutHandler(Handler):
    def get(self):
        cookie_val = "user_id=; Path=/"
        self.response.headers.add_header('Set-Cookie', cookie_val)
        self.redirect('/')