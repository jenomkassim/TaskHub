from google.appengine.ext import ndb


# from taskboard import TaskBoard


class MyUser(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    td_key = ndb.KeyProperty(repeated=True)
    td_name = ndb.StringProperty(repeated=True)
    td_creator_id = ndb.StringProperty(repeated=True)

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
