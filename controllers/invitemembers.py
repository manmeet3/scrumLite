# -*- coding: utf-8 -*-
# try something like
def invitemembers():
    form = SQLFORM(db.auth_membership)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form is invalid'
    return dict(form=form)
