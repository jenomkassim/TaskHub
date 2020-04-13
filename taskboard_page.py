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


# DEFAULT_TASKBOARD_NAME = 'default_taskboard'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

# def taskboard_key(taskboard_name=DEFAULT_TASKBOARD_NAME):
#     """Constructs a Datastore key for a Guestbook entity.
#
#     We use guestbook_name as the key.
#     """
#     return ndb.Key('Taskboard', taskboard_name)


class TaskBoardPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

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


        else:
            url = users.create_login_url(self.request.uri)
            login_status = 'Login'

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        taskboard_url_id = decrypted_idd.id()

        taskboard_ref = TaskBoard.get_by_id(taskboard_url_id, parent=decrypted_idd.parent())
        # taskboard_keys = taskboard_ref.creator_name
        # self.response.write(taskboard_keys)

        # SEARCH FOR USERS
        user_search = MyUser.query().fetch()


        template_values = {
            'url': url,
            'user': user,
            'welcome': welcome,
            'login_status': login_status,
            'user_email': user.email(),
            'user_search': user_search,
            'idd': idd,
            'taskboard_ref': taskboard_ref
        }

        template = JINJA_ENVIRONMENT.get_template('taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        idd = self.request.get('id')
        decrypted_idd = ndb.Key(urlsafe=idd)
        taskboard_url_id = decrypted_idd.id()

        taskboard_info = TaskBoard.get_by_id(taskboard_url_id, parent=myuser_key)
        this_taskboard_info_key = taskboard_info.key

        invitee_details = self.request.get('invitee_id')
        invitee_id = MyUser.get_by_id(invitee_details)

        invitee_id.td_key.append(taskboard_info.key)
        invitee_id.td_name.append(taskboard_info.name)
        invitee_id.td_creator_id.append(user.user_id())
        invitee_id.put()
        # self.response.write(taskboard_info.name)

        self.redirect('/taskboard?id=' + str(idd))
