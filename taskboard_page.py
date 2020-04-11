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

def taskboard_key(taskboard_name=DEFAULT_TASKBOARD_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Taskboard', taskboard_name)


class TaskBoardPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

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

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        taskboard_url_id = decrypted_idd.id()

        taskboard_details = ndb.Key('TaskBoard', taskboard_url_id).get()
        taskboard_details2 = ndb.Key('TaskBoard', taskboard_url_id)

        taskboard_info = TaskBoard.get_by_id(taskboard_url_id, parent=myuser_key)
        # self.response.write(TaskBoard.get_by_id(taskboard_url_id, parent=myuser_key))

        query = TaskBoard.query(ancestor=myuser_key)

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'all_taskboards': all_taskboards,
            'all_taskboards_count': all_taskboards_count,
            'taskboard_info': taskboard_info
        }

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
