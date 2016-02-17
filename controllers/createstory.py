@auth.requires_login()
def index():
    form = SQLFORM(db.story, fields=['user_story','story_points', 'created_on', 'created_by'])
    form.vars.team_id = auth.user_group(auth.user.id)
    form['_style']='border:1px solid black'
    if form.process().accepted:
        response.flash = 'story added'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'the forum is invalid'
    return dict(form=form)
