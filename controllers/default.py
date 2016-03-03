def index():
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
          return dict(stories=stories, tasks=tasks, sprint=sprint)
    else:
      msg = 'you do NOT belong to a team'
      return response.render('default/throw_error.html', dict(msg=msg))

def user():
    return dict(form=auth())
