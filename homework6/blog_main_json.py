
from handler import Handler
import json
from time import strftime

class BlogMainJson(Handler):
    def get(self):
        inputs = self.get_top_blog_inputs()
        json_str = []
        for input in inputs:
            temp = {}
            temp['title'] = input.subject
            temp['content'] = input.content
            temp['created'] = input.created.strftime('%c')
            temp['last-modified'] = input.last_modified.strftime('%c')
            json_str.append(temp)
        self.jwrite(json.dumps(json_str))
