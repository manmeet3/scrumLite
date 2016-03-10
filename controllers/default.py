from gluon.serializers import json

def index():
      return dict(message=T('ScrumLite Index page'))

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

  
