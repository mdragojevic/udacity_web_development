from handler import Handler
from db_models import User
import cgi
import re
from google.appengine.ext import db
import encoding as enc
from user_input_validation import validate_username, validate_password



class LoginHandler(Handler):
    def get(self):
        res = {
            "username": "",
            "error_name": "",
            "password": "",
            "error_pass": ""}
        self.render("login.html")

    def post(self):
        orig_user = self.request.get("username")
        username = cgi.escape(orig_user, quote=True)
        password = cgi.escape(self.request.get("password"), quote=True)
        
        name = validate_username(username)
        passw = validate_password(password)
        res = {
            "username": username,
            "error_name": "" if name else "That's not a valid username.",
            "password": password,
            "error_pass": "" if passw else "That wasn't a valid password.",
            }
        if name and passw:
            users = db.GqlQuery("SELECT * FROM User WHERE username=:1", username)
            correct_passw = ""
            for user in users:
                correct_passw = user.password
            if correct_passw and enc.validate_passw(password, correct_passw):
                user_key = str(user.key().id())
                hidden_key = enc.encode(user_key)
                cookie_val = str("user_id=%s|%s; Path=/" % (user_key,hidden_key))
                self.response.headers.add_header('Set-Cookie', cookie_val)
                self.redirect('/')
            elif not correct_passw:
                res["error_name"] = "User '%s' not registered." % username
                self.render("login.html", **res)
            else:
                res["error_pass"] = "Invalid password."
                self.render("login.html", **res)
        else:
            self.render("login.html", **res)