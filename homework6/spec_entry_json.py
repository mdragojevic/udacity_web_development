from handler import Handler
import json

class SpecificJson(Handler):
    def get(self, text_id):
        input = self.get_blog_input_by_id(text_id)[0]
        input_str={}
        if input:
            input_str['title'] = input.subject
            input_str['content'] = input.content
            input_str['created'] = input.created.strftime('%c')
            input_str['last-modified'] =input.last_modified.strftime('%c')
        self.jwrite(json.dumps(input_str))