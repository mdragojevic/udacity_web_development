
from handler import Handler
from google.appengine.ext import db
import json
from time import strftime

class BlogMainJson(Handler):
    def get(self):
        inputs = db.GqlQuery("SELECT * FROM BlogInput ORDER BY created DESC LIMIT 10")
        json_str = []
        for input in inputs:
            temp = {}
            temp['title'] = input.subject
            temp['content'] = input.content
            temp['created'] = input.created.strftime('%c')
            temp['last-modified'] = input.last_modified.strftime('%c')
            json_str.append(temp)
        self.jwrite(json.dumps(json_str))
