from handler import Handler
import json
from db_models import BlogInput

class SpecificJson(Handler):
    def get(self, text_id):
        input = BlogInput.get_by_id(int(text_id))
        input_str={}
        if input:
            input_str['title'] = input.subject
            input_str['content'] = input.content
            input_str['created'] = input.created.strftime('%c')
            input_str['last-modified'] =input.last_modified.strftime('%c')
        self.jwrite(json.dumps(input_str))