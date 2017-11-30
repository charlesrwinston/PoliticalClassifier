import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(open('tweets1.txt', 'r').read())


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
