import re 

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
MAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validate_username(username):
    return USER_RE.match(username)

def validate_password(pasword):
    return PASS_RE.match(pasword)

def validate_verify(password, verify):
    return password == verify

def validate_email(email):
    if email == "":
        return True
    return MAIL_RE.match(email)