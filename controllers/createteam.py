# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index():
        form = SQLFORM(db.Team)
        if form.process().accepted:
            group_id = auth.add_group(form.vars.Product_Name, form.vars.Product_Description)
            auth.add_membership(group_id, auth.user.id)
        elif form.errors:
            response.flash = 'form is invalid'
        return dict(form=form)
