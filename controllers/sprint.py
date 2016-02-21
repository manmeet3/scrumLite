@auth.requires_login()
def create_sprint():
    db.Sprint.team_id.default = auth.user_groups.keys()[0]
    form = SQLFORM(db.Sprint, fields=['sprint_name', 'start_date', 'end_date'])
    if form.process().accepted:
        response.flash = 'Sprint created'
        redirect(URL('index'))
    return dict(form=form)

def show_sprint():
    this_sprint = db.Sprint(request.args(0,cast=int)) or redirect(URL('index'))
    return dict(sprint=this_sprint)