from google.appengine.ext import ndb


class Task(ndb.Model):
    content = ndb.StringProperty(indexed=False)
    taskCreationDate = ndb.DateTimeProperty(auto_now_add=True)
