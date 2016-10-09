from handler import Handler

class BlogMainPage(Handler):
    def get(self):
        inputs, queried_last = self.get_top_blog_inputs()
        self.render("show_text.html", 
                    inputs=inputs, 
                    queried_last=queried_last)
