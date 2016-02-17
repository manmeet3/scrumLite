# -*- coding: utf-8 -*-
# try something like
@auth.requires_login()
def index():
        form = SQLFORM(db.Team, fields = ['Product_Owner', 'Product_Name', 'Team_Name', 'Team_Leader',
                                          'Product_Description'])
        if form.process().accepted:
            group_id = auth.add_group(form.vars.Product_Name, form.vars.Product_Description)
            auth.add_membership(group_id, auth.user.id)
            form.vars.Team_Group == group_id
        elif form.errors:
            response.flash = 'form is invalid'
        return dict(form=form)
