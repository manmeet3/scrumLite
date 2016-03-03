@auth.requires_login()
def create_sprint():
    if auth.user_groups.keys():
      db.Sprint.team_id.default = auth.user_groups.keys()[0]
      #print auth.user_groups.keys()[0]
    else:
      response.flash = 'null user group, sprint will NOT save'
      #redirect(URL('default', 'index'))
    form = SQLFORM(db.Sprint, fields=['sprint_name', 'start_date', 'end_date'])
    if form.process().accepted:
        response.flash = 'Sprint created'
        redirect(URL('default','index'))
    return dict(form=form)

def show_sprint():
    this_sprint = db.Sprint(request.args(0,cast=int)) or redirect(URL('index'))
    stories = db(this_sprint.id==db.Story.sprint_id).select(db.Story.ALL)
    return dict(sprint=this_sprint, stories=stories)

def view_all():
    stories = db((db.Sprint.team_id==db.Team.id) & (db.Team.team_group==auth.user_groups.keys()[0])).select(db.Sprint.ALL)
    return dict(stories=stories)
