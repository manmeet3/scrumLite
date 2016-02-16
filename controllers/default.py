def index():
    usrstories = db().select(db.story.ALL) #change to view team specific stories
    return dict(usrstories=usrstories)


def user():
    return dict(form=auth())

def show_story():
  this_story = db.story(request.args(0,cast=int)) or redirect(URL('index'))
  db.task.story_id.default = this_story.id
  form = SQLFORM(db.task).process() if auth.user else 'You need to log in'
  alltasks = db(db.task.story_id==this_story.id).select()
  return dict(story = this_story, tasks=alltasks, form=form)
