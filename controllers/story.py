@auth.requires_login()
def new_story():
    print "new_story called"
    if auth.user_groups.keys():
      db.Story.team_id.default = auth.user_groups.keys()[0]
    else:
      response.flash = 'NULL USER GROUP, story will NOT save'

    if request.args(0) is not None:
      db.Story.sprint_id.default = request.args(0,cast=int)
      db.Story.backlogged.default = False
    else:
      db.Story.backlogged.default = True

    form = SQLFORM(db.Story, fields=['user_story', 'created_on', 'created_by'])
    if form.process().accepted:
        response.flash = 'story added'
        if request.args(0) is not None:
          redirect(URL('sprint', 'show_sprint', args=request.args(0,cast=int)))
        else:
          redirect(URL('team', 'backlog'))
    elif form.errors:
        response.flash = 'the form is invalid'

    return dict(form=form)

def show_story():
  this_story = db.Story(request.args(0,cast=int)) or redirect(URL('index'))
  db.Task.story_id.default = this_story.id

  form = SQLFORM(db.Task) if auth.user else 'You need to log in'
  if form.process().accepted:
    new_pts = this_story.story_points + int(form.vars.task_points)
    this_story.update_record(story_points = new_pts)
    response.flash = 'task added'

  alltasks = db(db.Task.story_id==this_story.id).select()
  if alltasks is None:
    this_story.update_record(completed='True')

  size=len(alltasks)
  #print size
  for task in alltasks:
    if task.status=="Done":
      size = size - 1
      #print size
  if size == 0:
    #print 'updating'
    this_story.update_record(completed='True')
  else:
    this_story.update_record(completed='False')
  db.Story.backlogged.show_if = (db.Story.backlogged==True)

  if auth.user_groups.keys():
    this_team_sprints = ((auth.user_groups.keys()[0]==db.Team.team_group) & (db.Sprint.team_id==db.Team.id))
    db.Story.sprint_id.requires=IS_EMPTY_OR(IS_IN_DB(db(this_team_sprints), 'Sprint.id', '%(sprint_goal)s'))
  movestory=SQLFORM(db.Story, this_story, showid=False, fields=['sprint_id'])
  if movestory.process().accepted:
     this_story.update_record(backlogged='False')
     response.flash = 'Story moved'

  return dict(story = this_story, tasks=alltasks, form=form, movestory=movestory)

def show_task():
    this_task = db.Task(request.args(0,cast=int)) or redirect(URL('index'))
    task_story = db.Story(this_task.story_id)
    form = SQLFORM(db.Task, this_task, showid=False, fields=['status', 'description', 'task_points', 'assigned'])
    this_comments = db(db.Comments.task_id == this_task).select()
    comments_form = SQLFORM(db.Comments, fields=['comment'])
    comments_form.vars.task_id = this_task
    if comments_form.process().accepted:
        response.flash = 'added comment'
    if form.process().accepted:
        response.flash = 'task changed'
        redirect(URL('story', 'show_story', args=task_story.id))
    return dict(task=this_task, story=task_story, form=form, this_comments=this_comments, comments_form=comments_form)

def move_to_backlog():
    this_story = db.Story(request.args(0,cast=int)) or redirect(URL('index'))
    this_story.update_record(backlogged='True')
    this_story.update_record(sprint_id=None)
