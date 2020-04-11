from google.appengine.ext import ndb


class Task(ndb.Model):
    task = ndb.StringProperty(indexed=False)
    due_date = ndb.DateProperty()
    taskCreationDate = ndb.DateTimeProperty(auto_now_add=True)
