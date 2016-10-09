import webapp2
from handler import Handler
import encoding as enc

class WelcomeHandler(Handler):
    def get(self):
        cookie_val = self.request.cookies.get('user_id')
        username, hidden = cookie_val.split('|')
        if enc.validate(username, hidden):
            self.render("welcome.html", username = username)
        else:
            self.redirect('/blog/signup')