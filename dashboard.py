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

            taskboard_user_ref = MyUser.get_by_id(myuser_key.id())
            taskboard_user_keys = taskboard_user_ref.td_key

            # for i in taskboard_user_keys:
            #     # creator_key = ndb.Key('MyUser', i.td_creator_id)
            #     j = TaskBoard.get_by_id(i.id(), parent=i.parent())
            #     self.response.write(j.name)
            #     self.response.write('<br/>')

        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'taskboard_user_keys': taskboard_user_keys,
            'myuser_key': myuser_key,
            'TaskBoard': TaskBoard
            # 'all_taskboards': all_taskboards,
            # 'all_taskboards_count': all_taskboards_count
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

        # Ask Datastore to allocate an ID.
        new_id = ndb.Model.allocate_ids(size=1, parent=myuser_key)[0]

        # Datastore returns us an integer ID that we can use to create the new taskboard
        # key
        new_taskboard_key = ndb.Key('TaskBoard', new_id, parent=myuser_key)

        # Now we can put the message into Datastore
        new_taskboard = TaskBoard(key=new_taskboard_key, creator=myuser_key, creator_name=user.email(),
                                  name=taskboard_title, creator_id=user.user_id())
        new_taskboard.put()
        new_taskboard_user_ref = MyUser.get_by_id(myuser_key.id())
        new_taskboard_user_ref.td_key.append(new_taskboard.key)
        new_taskboard_user_ref.td_name.append(taskboard_title)
        new_taskboard_user_ref.td_creator_id.append(user.user_id())
        new_taskboard_user_ref.put()
        self.redirect('/dashboard')

