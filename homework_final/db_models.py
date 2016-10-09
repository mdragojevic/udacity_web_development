from google.appengine.ext import db

class WikiPage(db.Model):
    page = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created =db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created =db.DateTimeProperty(auto_now_add = True)