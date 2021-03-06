import os
from web3py import action, request, DAL, Field, Session, Cache

# define session and cache objects
session=Session(secret = 'some secret')
cache = Cache(size=1000)

# define database and tables
db = DAL('sqlite://storage.db', folder=os.path.join(os.path.dirname(__file__), 'databases'))
db.define_table('todo', Field('info'))

# example index page using session, template and vue.js
@action('/$app_name/index', view='index.html', fixtures=[session])
def index():
    session['counter'] = session.get('counter', 0) + 1
    return dict(session=session)

# example of GET/POST/DELETE RESTful APIs
@action('/$app_name/api', fixtures=[db])
def todo():
    return dict(items=db(db.todo).select(orderby=~db.todo.id).as_list())

@action('/$app_name/api', method='POST', fixtures=[db])
def todo():
    return dict(id=db.todo.insert(info=request.json.get('info')))

@action('/$app_name/api/<id>', method='DELETE', fixtures=[db, session])
def todo(id):   
    db(db.todo.id==id).delete()
    return dict()

# example of caching
@action('/$app_name/uuid')
@cache.memoize(expiration=5)
def uuid():
    import uuid
    return str(uuid.uuid4())
