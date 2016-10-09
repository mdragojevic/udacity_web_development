from handler import Handler
from db_models import BlogInput

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