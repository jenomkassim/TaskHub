from google.appengine.ext import ndb


# from taskboard import TaskBoard


class MyUser(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    td_key = ndb.KeyProperty(repeated=True)
    # td_name = ndb.StringProperty(repeated=True)
    td_creator_id = ndb.StringProperty(repeated=True)

