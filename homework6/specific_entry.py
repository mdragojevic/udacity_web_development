
from handler import Handler

class SpecificEntry(Handler):
    def get(self, text_id):
        # get obj id from get request
        # find in db: get_by_id()
        input, queried_last = self.get_blog_input_by_id(text_id)
        if input:
            input = [input]
            self.render("show_text.html", inputs=input, queried_last=queried_last)