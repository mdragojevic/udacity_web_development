import jinja2
import os
import webapp2
import cgi
from google.appengine.ext import db
from google.appengine.api import memcache
from db_models import WikiPage, User
import encoding as enc

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
                               #autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def jwrite(self, jstring):
        self.response.headers['Content-Type'] = 'application/json'
        self.write(jstring)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        cookie = self.request.cookies.get('user_id')
        self.user = None
        if cookie:
            uid, coded_val = cookie.split('|')
            if (enc.validate(uid, coded_val)):
                self.user = User.get_by_id(int(uid))

    def get_versions_ascending(self, url):
        pages = db.GqlQuery("SELECT * FROM WikiPage WHERE page=:1 ORDER BY created ASC", url)
        page_versions = []
        for p in pages:
            page_versions.append(p)
        return page_versions

    def get_wiki_page(self, url, version=-1):
        page_versions = memcache.get(url)
        if page_versions is None:
            page_versions = self.get_versions_ascending(url)
            if page_versions == []:
                return None
            memcache.set(url, page_versions)
        return page_versions[version]

    def get_content(self, url, version=-1):
        page = self.get_wiki_page(url, version)
        return "" if page is None else cgi.escape(page.content, quote=True)

    def edit_wiki_page(self, url, content, version=-1):
        wiki = self.get_wiki_page(url, version)
        wiki = WikiPage(page = url, 
                        content=content)
        wiki.put()
        page_versions = memcache.get(url)
        if page_versions is None:
            page_versions = self.get_versions_ascending(url)
        page_versions.append(wiki)
        memcache.set(url, page_versions)

