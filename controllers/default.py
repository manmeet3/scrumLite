from gluon.serializers import json
import chats


def index():
    return chats.index(db)


@auth.requires_signature()
def message_new():
    return chats.message_new(db)


@auth.requires_signature()
def message_updates():
    # need to unlock the session when using
    # session file, should not be need it when
    # using session in db, or in a cookie
    session._unlock(response)
    return chats.message_updates(db)


def user():
    return dict(form=auth())

def show_sprint():
  if auth.user_groups.keys():
      sprint = db((db.Sprint.team_id==db.Team.id) & (db.Team.team_group==auth.user_groups.keys()[0])
      & (db.Sprint.start_date < request.now) & (db.Sprint.end_date > request.now)).select(db.Sprint.ALL).first()
      try:
          sprint.id
      except AttributeError:
          msg = 'No active Sprints found for your team'
          message = dict(msg=msg)
          return response.render('default/throw_error.html', message)
      else:
          stories = db(sprint.id==db.Story.sprint_id).select(db.Story.ALL)
          tasks = db((sprint.id==db.Story.sprint_id) & (db.Task.story_id==db.Story.id)).select(db.Task.ALL)
          backlogs = db((db.Story.team_id==auth.user_groups.keys()[0]) & (db.Story.backlogged==True)).select(db.Story.ALL)
          return dict(stories=stories, tasks=tasks, sprint=sprint, backlogs=backlogs)
  else:
      msg = 'you need to CREATE/JOIN a Team'
      return response.render('default/throw_error.html', dict(msg=msg))

  