import webapp2
import codecs
import cgi
import re

form = """
<h1>Enter some text to ROT13:</h1>
<form method="post">
<textarea style="height:200px; width:280px;"  name="text">%(text_val)s</textarea>
<br>
<input type="submit"></input>
</form>
"""

link_txt = """
<h1>Udacity homework 2</h1>
<ul>
	<li>
		<a href="/rot13">ROT13 solution</a>
	</li>
    <li>
        <a href="/signup">SignUp solution</a>
    </li>
</ul>
"""

signup = """
<h1>Signup</h1>
<form method="post">
<label style="display: inline-block; width: 280px; text-align: right; padding:2px;">
    Username
    <input name="username" value="%(username)s">
    </input>
</label>
<span style="color: red;">%(error_name)s</span>
<br>
<label style="display: inline-block; width: 280px; text-align: right; padding:2px;">
    Password
    <input name="password" type="password" value="%(password)s"></input>
</label>
<span style="color: red;">%(error_pass)s</span> 
<br>
<label style="display: inline-block; width: 280px; text-align: right; padding:2px;">
    Verify password
    <input name="verify" type="password" value="%(verify)s"></input> 
</label>
<span style="color: red;">%(error_ver)s</span>
<br>
<label style="display: inline-block; width: 280px; text-align: right; padding:2px;">
    Email (optional)
        <input name="email" value="%(mail)s"></input>
</label>
<span style="color: red;">%(error_mail)s</span>  
<br>
<br>
<input type="submit"></input>
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

class Rot13Handler(webapp2.RequestHandler):
    def get(self):
        self.write_form()
        
    def write_form(self, val=""):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(form % {"text_val": val})

    def post(self):
        text = self.request.get("text")
        new_text = codecs.encode(text,"rot13")
        self.write_form(new_text)

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        res = {
            "username": "",
            "error_name": "",
            "password": "",
            "error_pass": "",
            "verify": "",
            "error_ver": "",
            "mail": "",
            "error_mail": ""}
        self.write_signup(res)

    def write_signup(self, res):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(signup % res)

    def validate_username(self, username):
        return USER_RE.match(username)

    def validate_password(self, pasword):
        return PASS_RE.match(pasword)

    def validate_verify(self, password, verify):
        return password == verify

    def validate_email(self, email):
        if email == "":
            return True
        return MAIL_RE.match(email)

    def post(self):
        orig_user = self.request.get("username")
        username = cgi.escape(orig_user, quote=True)
        password = cgi.escape(self.request.get("password"), quote=True)
        verify = cgi.escape(self.request.get("verify"), quote=True)
        email = cgi.escape(self.request.get("email"), quote=True).strip()

        name = self.validate_username(username)
        passw = self.validate_password(password)
        ver = self.validate_verify(password, verify)
        mail = self.validate_email(email)
        res = {
            "username": username,
            "error_name": "" if name else "That's not a valid username.",
            "password": password,
            "error_pass": "" if passw else "That wasn't a valid password.",
            "verify": verify,
            "error_ver": "" if not passw or ver else "Your passwords didn't match.",
            "mail": email,
            "error_mail": "" if mail else "That's not a valid email."
            }
        if (name and passw and ver and mail):
            self.redirect('/welcome?username=%s' % orig_user )
        else:
            self.write_signup(res)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write("<h1>Welcome, %s</h1" % username)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(link_txt)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rot13', Rot13Handler),
    ('/signup', SignUpHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
