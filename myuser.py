from google.appengine.ext import ndb


class MyUser(ndb.Model):
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    td_key = ndb.KeyProperty(repeated=True)

