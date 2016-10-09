from handler import Handler

class WikiHandler(Handler):
    def get(self, url):
        ver = self.request.get("v")
        page = None
        if not ver.isdigit():
            page = self.get_wiki_page(url)
            url_mod = url
        else:
            page = self.get_wiki_page(url, int(ver))
            url_mod = url + '?v=' + url_mod
            if url is "/" and page is None:
                content = "<h1>Welcome to main Wiki page</h1>"
                self.edit_wiki_page("/", content)
                page = self.get_wiki_page(url)
        if page is None:
            self.redirect("/_edit" + url)
        else:
            self.render("wiki.html",  history=True, user=(self.user != None), url=url, content=page.content)