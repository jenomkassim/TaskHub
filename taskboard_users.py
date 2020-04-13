from google.appengine.ext import ndb

from taskboard import TaskBoard


class TaskBoardUsers(ndb.Model):
    tb_key = ndb.KeyProperty(kind=TaskBoard)
    tb_name = ndb.StringProperty()
    tb_creator = ndb.StringProperty()
    user_email = ndb.StringProperty()
    user_id = ndb.StringProperty()
    status = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
