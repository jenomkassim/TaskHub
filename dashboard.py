import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Dashboard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        welcome = 'Welcome back to the workspace, we missed You!'
        login_status = ''

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the workspace, we hope you enjoy our application!'
                myuser = MyUser(id=user.user_id())
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status
        }

        template = JINJA_ENVIRONMENT.get_template('dashboard.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     self.response.headers['Content-Type'] = 'text/html'
    #
    #     action = self.response.get('button')
    #
    #     if action == 'Search':
    #         name = self.request.get('vehicleName')
    #         manufacturer = self.request.get('manufacturer')
    #         lower_year = self.request.get('lower-year')
    #         upper_year = self.request.get('upper-year')
    #         battery_lower = self.request.get('battery-lower')
    #         battery_upper = self.request.get('battery-upper')
    #         range_lower = self.request.get('range-lower')
    #         range_upper = self.request.get('range-upper')
    #         cost_lower = self.request.get('cost-lower')
    #         cost_upper = self.request.get('cost-upper')
    #         power_lower = self.request.get('power-lower')
    #         power_upper = self.request.get('power-upper')
    #
    #     car_query = Vehicles.query()
