from handler import Handler
import logging
class EditHandler(Handler):
    def get(self, url):
        ver = self.request.get("v")
        if self.user == None:
            if self.get_wiki_page(url):
                self.redirect(url)
            self.redirect('/')
        if not ver.isdigit():
            content = self.get_content(url)
            url_mod = url
        else:
            content = self.get_content(url, int(ver))
            url_mod = url + '?v=' + ver
        self.render("form.html",  history=True, user=(self.user != None), url=url_mod, content=content)
        self.url = url

    def post(self, url):
        content = self.request.get("content")
        self.edit_wiki_page(url, content)
        self.redirect(url)