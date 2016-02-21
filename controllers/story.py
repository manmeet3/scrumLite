@auth.requires_login()
def new_story():
    db.Story.team_id.default = auth.user_group(auth.user.id)
    form = SQLFORM(db.Story, fields=['user_story','story_points', 'created_on', 'created_by'])
    form['_style']='border:1px solid black'
    if form.process().accepted:
        response.flash = 'story added'
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

