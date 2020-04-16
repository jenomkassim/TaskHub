from google.appengine.ext import ndb


class Task(ndb.Model):
    title = ndb.StringProperty()
    due_date = ndb.DateProperty()
    status = ndb.BooleanProperty()
    assignee_id = ndb.StringProperty()
    taskCreationDate = ndb.DateTimeProperty(auto_now_add=True)
