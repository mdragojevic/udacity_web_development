from handler import Handler
from db_models import User
import cgi
from google.appengine.ext import db
import encoding as enc
from user_input_validation import *

class RegistrationHandler(Handler):
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
        self.render("registration.html")

    def post(self):
        orig_user = self.request.get("username")
        username = cgi.escape(orig_user, quote=True)
        password = cgi.escape(self.request.get("password"), quote=True)
        verify = cgi.escape(self.request.get("verify"), quote=True)
        email = cgi.escape(self.request.get("email"), quote=True).strip()

        name = validate_username(username)
        passw = validate_password(password)
        ver = validate_verify(password, verify)
        mail = validate_email(email)
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
        exists = False
        if name:
            # check if user exists in the User db
            users = db.GqlQuery("SELECT * FROM User WHERE username=:1", username)
            user_len = 0
            for user in users:
                user_len +=1
            exists = user_len != 0

        if name and passw and ver and mail and not exists:
            user = User(username=username,
                        password=enc.hash_passw(password),
                        email=email)
            user.put()
            hidden_user = enc.encode(orig_user)
            cookie_val = str("user_id=%s|%s; Path=/" % (orig_user,hidden_user))
            self.response.headers.add_header('Set-Cookie', cookie_val)
            self.redirect('/blog/welcome')
        else:
            if exists:
                res["error_name"] = "Username '%s' already taken." % username
            self.render("registration.html", **res)