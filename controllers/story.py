@auth.requires_login()
def new_story():
    if auth.user_groups.keys():
      db.Story.team_id.default = auth.user_groups.keys()[0]
      print auth.user_groups.keys()[0]
    else:
      response.flash = 'NULL USER GROUP, story will NOT save'
    db.Story.sprint_id.default = request.args(0,cast=int)
    form = SQLFORM(db.Story, fields=['user_story','story_points', 'created_on', 'created_by'])
    form['_style']='border:1px solid black'
    if form.process().accepted:
        response.flash = 'story added'
        redirect(URL('sprint', 'show_sprint', args=request.args(0,cast=int)))
        print request.env.http_referer
    elif form.errors:
        response.flash = 'the form is invalid'
    return dict(form=form)

def show_story():
  this_story = db.Story(request.args(0,cast=int)) or redirect(URL('index'))
  db.Task.story_id.default = this_story.id
  form = SQLFORM(db.Task).process() if auth.user else 'You need to log in'
  alltasks = db(db.Task.story_id==this_story.id).select()
  return dict(story = this_story, tasks=alltasks, form=form)

def show_task():
    this_task = db.Task(request.args(0,cast=int)) or redirect(URL('index'))
    task_story = db.Story(this_task.story_id)
    form = SQLFORM(db.Task, this_task, fields=['status'])
    if form.process().accepted:
        response.flash = 'task changed'
        redirect(URL('index'))
    return dict(task=this_task, story=task_story, form=form)
