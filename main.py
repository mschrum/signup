import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
            .error {
                color: red;
            }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
SignUp_form = """
<form action="/" method="post">
    <table>
        <tbody>
            <tr>
                <td>
                    <label>User Name:</label>
                </td>
                <td>
                    <input type="text" name="username" value="{0}"/>
                    <span class="error">{2}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label>Password:</label>
                </td>
                <td>
                    <input type="password" name="password"/>
                    <span class="error" >{3}</span>
                </td>
            </tr>
                <td>
                    <label>Verify Password:</label>
                </td>
                <td>
                    <input type="password" name="verify"/>
                    <span class="error">{4}</span>
                </td>
            </tr>
                <td>
                    <label>E-mail Address:</label>
                </td>
                <td>
                    <input type="text" name="email" value="{1}"/>
                    <span class="error">{5}</span>
                </td>
            </tr>
                <td>
                    <input type="submit" value="Submit"/>
                </td>
            </tr>
        </tbody>
    </table>
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$" )
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    def get(self):
        response = page_header + SignUp_form.format("","","","","","") + page_footer
        self.response.write(response)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        error_user = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        params = dict(username = username, email = email)

        if not valid_username(username):
            error_user = "That's not a valid Username."
            have_error = True
        if not valid_password(password):
            error_password = "That's not a valid password."
            have_error = True
        elif password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True
        if not valid_email(email):
            error_email = "That's not a valid e-mail"
            have_error = True
        if have_error:
            response = page_header + SignUp_form.format(username, email, error_user, error_password, error_verify, error_email) + page_footer
            self.response.write(response)
        else:
            self.redirect("/welcome?username=" + username)
class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Signup</title>
            </head>
            <body>
                <h2>Welome {0}</h2>
            </body>
            </head>
            </html>
            """
            self.response.write(response.format(username))
        else:
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
