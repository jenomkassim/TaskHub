from google.appengine.ext import ndb


class MyUser(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

# class Task(ndb.Model):
#     task = ndb.StringProperty(indexed=False)
#     due_date = ndb.DateProperty()
#     taskCreationDate = ndb.DateTimeProperty(auto_now_add=True)
#
#
# class TaskBoard(ndb.Model):
#     creator = ndb.KeyProperty(kind=MyUser)
#     name = ndb.StringProperty()
#     tasks = ndb.StructuredProperty(Task, repeated=True)
#     date = ndb.DateTimeProperty(auto_now_add=True)
