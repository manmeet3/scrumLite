def index():
    sprints = db().select(db.Sprint.ALL)
    stories = db().select(db.Story.ALL)
    tasks = db().select(db.Task.ALL)
    return dict(stories=stories, tasks=tasks, sprints=sprints)

def user():
    return dict(form=auth())

