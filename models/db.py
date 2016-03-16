from gluon.tools import Auth, Service, PluginManager,prettydate
import os

db = DAL("sqlite://storage.sqlite")
response.generic_patterns = ['*'] if request.is_local else []
auth = Auth(db, hmac_key=Auth.get_or_create_key())
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables()
#auth.settings.extra_fields['auth_user']= [Field('Pic','upload'),Field('About_Me','text')]


## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# modify default policy on creating unique groups for each user
auth.settings.create_user_groups = None



if auth.user_id != None:
    setGroup=auth.user_groups.copy()
elif auth.user_id is None:
    setGroup=["None","You Need to Log In"]
    
from gluon.contrib.login_methods.rpx_account import RPXAccount
auth.settings.actions_disabled=['register', 'change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request,
    api_key='73dab71b7fdfc0f49c10f8e64ee6a5adcf66b2c3',
    domain='ScrumLite',
    url = "http://scrumlite.rpxnow.com/%s/default/user/login" % request.application)

db.define_table('images',
    Field('image', 'upload', uploadfolder=os.path.join(request.folder,'uploads')),
    Field('user',db.auth_user))

db.images.user.writable = db.images.user.readable = False

db.define_table('Team',
  Field('product_owner', 'reference auth_user', default=auth.user_id, writable = False),
  Field('product_name', requires = IS_NOT_EMPTY()),
  Field('team_name', requires = IS_NOT_EMPTY()),
  Field('team_leader', 'reference auth_user'),
  Field('team_group', 'reference auth_group'),
  Field('product_description', 'text', requires = IS_NOT_EMPTY()),
               format='%(team_name)s')

db.Team.id.readable = False

db.define_table('Sprint',
  Field('sprint_name'),
  Field('start_date', 'date'),
  Field('end_date', 'date'),
  Field('team_id', 'reference Team'),
                format='%(sprint_name)s')

db.define_table('Story',
  Field('backlogged', type = 'boolean', default = 'True'),
  Field('sprint_id', 'reference Sprint', default=None),
  Field('team_id', 'reference Team'),
  Field('user_story','text', requires = IS_NOT_EMPTY()),
  Field('story_points','integer', default=0),
  Field('completed', type = 'boolean', default = 'False', readable=False),
  Field('created_on', 'datetime', default=request.now, writable = False),
  Field('created_by', 'reference auth_user', default=auth.user_id),
  )

db.Story.sprint_id.readable = False
db.Story.completed.readable = False
db.Story.created_by.writable = False

db.define_table('Task',
  Field('name', requires = IS_NOT_EMPTY()),
  Field('status','string', requires=IS_IN_SET(["To do", "In progress", "Done"]), default="To do"),
  Field('assigned', 'reference auth_user', default=None),
  Field('task_creation_time', 'datetime', default=request.now, writable = False),
  Field('estimated_completion_time', 'datetime', requires = IS_DATETIME()),
  Field('task_points', 'integer', requires=IS_IN_SET(['0','1','2','3','5','8','13','21'])),
  Field('story_id', 'reference Story')
  )
if auth.user_groups.keys():
      query = ((db.auth_group.id==auth.user_groups.keys()[0]) & (db.auth_group.id==db.auth_membership.group_id) & (db.auth_membership.user_id==db.auth_user.id))
      db.Task.assigned.requires=IS_EMPTY_OR(IS_IN_DB(db(query), db.auth_user, '%(first_name)s'))
db.Task.story_id.writable = db.Task.story_id.readable = False

db.define_table('Invitations',
    Field('to_user', 'reference auth_user'),
    Field('from_user', 'reference auth_user', default=auth.user_id),
    Field('from_group', 'reference auth_group'))

#db.define_table('TSR',Field('Team','integer', writable=False),Field('Time_Period'),Field('Weekly_Summarization', 'text', requires = IS_NOT_EMPTY()))

Post= db.define_table("post",
        Field("message", "text", requires=IS_NOT_EMPTY(), notnull=True),
        auth.signature)
Post.is_active.readable = False
Post.is_active.writable = False
