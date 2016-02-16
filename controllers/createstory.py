@auth.requires_login()
def index():
    form = SQLFORM(db.story)
    form.vars.Team = auth.user_group(auth.user.id)
    if form.process().accepted:
        response.flash = 'story added'
    elif form.errors:
        response.flash = 'the forum is invalid'
    return dict(form=form)
