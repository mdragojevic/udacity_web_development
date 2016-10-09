import jinja2
import os
import webapp2
from google.appengine.ext import db
from google.appengine.api import memcache
from db_models import BlogInput
import time

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def jwrite(self, jstring):
        self.response.headers['Content-Type'] = 'application/json'
        print jstring
        self.write(jstring)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))

    def get_top_blog_inputs(self, update=False):
        key = 'top'
        inputs = memcache.get(key)
        queried_last = 0
        if inputs is None or update:
            print "DB QUERY!!!"
            inputs = list(db.GqlQuery("SELECT * FROM BlogInput ORDER BY created DESC LIMIT 10"))
            memcache.set(key, inputs)
            memcache.set('time', time.time())
        else:
            t = memcache.get('time')
            if t:
                queried_last = int(time.time() - t)
        return inputs, queried_last

    def get_blog_input_by_id(self, id):
        input = memcache.get(id)
        queried_last = 0
        if input is None:
            input = BlogInput.get_by_id(int(id))
            memcache.set(id, input)
            memcache.set(id + '_time', time.time())
        else:
            t = memcache.get(id + '_time')
            if t:
                queried_last = int(time.time()-t)
        return input, queried_last

