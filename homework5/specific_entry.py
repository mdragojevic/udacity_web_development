
from handler import Handler
from db_models import BlogInput

class SpecificEntry(Handler):
    def get(self, text_id):
        # get obj id from get request
        # find in db: get_by_id()
        input = BlogInput.get_by_id(int(text_id))
        if input:
            input = [input]
            self.render("show_text.html", inputs=input)