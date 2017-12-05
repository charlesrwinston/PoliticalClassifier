import webapp2
from flask import Flask, render_template
#app = Flask(__name__)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello World')

class Home(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Home')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/home', Home),
], debug=True)
