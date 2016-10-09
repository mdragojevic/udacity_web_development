from handler import Handler
from google.appengine.api import memcache
import cgi

class HistoryHandler(Handler):
    def get(self, url):
        versions = memcache.get(url)
        page_versions = []
        
        for idx, ver in enumerate(versions):
            tmp = {}
            tmp['created'] = ver.created.strftime('%H:%M:%S %d.%b.%y')
            tmp['content'] = cgi.escape(ver.content, quote=True)[0:300]
            tmp['idx'] = idx
            print tmp
            page_versions.append(tmp)
        page_versions.reverse()
        self.render("history.html", user=(self.user != None), history=False, url=url, page_versions=page_versions)