# spring plan database table
db.define_table('sprint_plan',
  Field('Heading', requires = IS_NOT_EMPTY()),
  Field('Goal', 'text'),
  Field('created_on', 'datetime', default=request.now),
  Field('created_by', 'reference auth_user', default=auth.user_id),
  )


#--------------------------------- spring review --------------
db.define_table('sprint_review',
  Field('Things_that_did_not_work', 'text'),
  Field('Things_that_worked', 'text'),
  Field('Things_to_keep_doing', 'text'),
  Field('Unfinished_work', 'text'),
  Field('Work_completion_rate', 'text')
  )
