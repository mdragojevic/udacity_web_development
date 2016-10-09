import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))

class BlogInput(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created =db.DateTimeProperty(auto_now_add = True)
    date = db.DateProperty(auto_now_add = True)

class MainPage(Handler):
    def get(self):
        inputs = db.GqlQuery("SELECT * FROM BlogInput ORDER BY created DESC")
        self.render("show_text.html", inputs=inputs)

class NewPost(Handler):
    def get(self):
        self.render("form.html")
        #render form

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            input = BlogInput(subject=subject, content=content)
            input.put()
            self.redirect('/blog/%d' % input.key().id())
        else:
            error = "Both title and content are required to submit a new text!"
            self.render("form.html", subject=subject, content=content, error=error)

class SpecificEntry(Handler):
    def get(self, text_id):
        # get obj id from get request
        # find in db: get_by_id()
        input = BlogInput.get_by_id(int(text_id))
        if input:
            input = [input]
            self.render("show_text.html", inputs=input)

class MainHandler(Handler):
    def get(self):
        self.write('<h1><a href="/blog">Check out my blog!</a></h1>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainPage),
    ('/blog/newpost', NewPost),
    ('/blog/(\d+)', SpecificEntry)
], debug=True)
