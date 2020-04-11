from google.appengine.ext import ndb

from myuser import MyUser
from task import Task


class TaskBoard(ndb.Model):
    creator = ndb.KeyProperty(kind=MyUser)
    creator_name = ndb.StringProperty()
    creator_id = ndb.StringProperty()
    name = ndb.StringProperty()
    tasks = ndb.StructuredProperty(Task, repeated=True)
    date = ndb.DateTimeProperty(auto_now_add=True)