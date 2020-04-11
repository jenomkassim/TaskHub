import os

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from taskboard import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

DEFAULT_TASKBOARD_NAME = 'default_taskboard'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def myuser_parent_key(taskboard_name=DEFAULT_TASKBOARD_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('MyUser', taskboard_name)


class Dashboard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # taskboard_name = self.request.get('taskboard_name',
        #                                   DEFAULT_TASKBOARD_NAME)
        # taskboard_query = TaskBoard.query(
        #     ancestor=taskboard_key(taskboard_name)).order(-TaskBoard.date)
        #
        # taskboards = taskboard_query.fetch()

        url = ''
        welcome = ''
        login_status = ''

        user = users.get_current_user()

        # taskboard_key = ndb.Key('TaskBoard', taskboard_title, parent=myuser_key)
        # myuser_key = ndb.Key('MyUser', user.user_id())
        # myuser = myuser_key.get()
        # self.response.write(myuser_key)

        if user:
            welcome = 'Welcome back to the workspace, we missed You!'
            url = users.create_logout_url('/')
            login_status = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Hurray! Your First Login into the workspace, we hope you enjoy our application!'
                myuser = MyUser(id=user.user_id(),
                                identity=user.user_id(),
                                email=user.email())
                myuser.put()

            all_taskboards = TaskBoard.query(ancestor=myuser_key).fetch()
            all_taskboards_count = TaskBoard.query(ancestor=myuser_key).count()


        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'all_taskboards': all_taskboards,
            'all_taskboards_count': all_taskboards_count
        }

        template = JINJA_ENVIRONMENT.get_template('dashboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # GET USER KEY
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())

        # GET NEW TASKBOARD NAME
        taskboard_title = self.request.get('taskboard_name')

        # CREATE NEW TASKBOARD
        new_taskboard_key = ndb.Key('TaskBoard', taskboard_title, parent=myuser_key)
        new_taskboard = TaskBoard(key=new_taskboard_key, creator=myuser_key, creator_name=user.email(),
                                  creator_id=user.user_id(),
                                  name=taskboard_title)

        # COMMIT NEW TASKBOARD TO DATASTORE
        new_taskboard.put()
        self.redirect('/dashboard')

        # taskboard_key = ndb.Key('TaskBoard', taskboard_title, parent=myuser_key)
        # new_taskboard = taskboard_key

        # if taskboard_title == TaskBoard.get_by_id(taskboard_key.id()):
        #     self.response.write('Taskboard Exists')
        # else:
        #     self.response.write('New Taskboard')

        # self.response.write(TaskBoard.get_by_id(myuser_key.id()))
        # new_taskboard.put()
        # self.redirect('/dashboard')

        # self.response.write(new_taskboard.creator)
        # self.response.write('<br/>')
        # self.response.write(new_taskboard.name)

        # self.response.write(taskboard_key)

        # if user:
        #     taskboard.name = taskboard_title
        #     taskboard.put()
        #     self.redirect('/dashboard')
        # self.response.write(taskboard_title)
