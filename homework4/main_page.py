from handler import Handler
from google.appengine.ext import db

class BlogMainPage(Handler):
    def get(self):
        inputs = db.GqlQuery("SELECT * FROM BlogInput ORDER BY created DESC")
        self.render("show_text.html", inputs=inputs)
