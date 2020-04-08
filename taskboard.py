from google.appengine.ext import ndb

from myuser import MyUser
from task import Task


class TaskBoard(ndb.Model):
    author = ndb.StructuredProperty(MyUser)
    tasks = ndb.StructuredProperty(Task)
    date = ndb.DateTimeProperty(auto_now_add=True)
