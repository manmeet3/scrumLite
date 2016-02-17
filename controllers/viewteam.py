# -*- coding: utf-8 -*-
# try something like
def index():
    db.auth_user.id.readable = False
    db.auth_user.password.readable = False
    db.auth_user.registration_key.readable = False
    db.auth_user.reset_password_key.readable = False
    db.auth_user.registration_id.readable = False
    rows = db((db.auth_membership.user_id == db.auth_user.id)&(db.auth_group.id == db.auth_membership.group_id)).select(db.auth_user.ALL)
    return dict(rows=rows)
    #return dict(grid=SQLFORM.grid(db.auth_membership.user_id == db.auth_user.id)&(db.auth_group.id == db.auth_membership.group_id))
