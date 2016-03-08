import datetime

def plugin_google_chart():
    """used with the .load view to create a google chart
    Because this is used in a view LOAD, parameters are passed back from the browser as vars in the URL
    The complulsory vars include: 'type', a string defining the chart_type
        'data_url', which is a URL of the function which returns the data to be charted

    The use in the view is like this (including an example data URL

    {{ data_url = URL('plugin_google_chart','plugin_return_data.json',user_signature=True)}}
    ...
    {{=LOAD('plugin_google_chart','plugin_google_chart.load',ajax=True,
        user_signature=True,vars={'type':'bar','data_url':data_url})}}
    """
    chart_type = request.vars.type
    data_url = request.vars.data_url
    options_dict = request.vars.options_dict or ''
    if chart_type and data_url:
        return dict(chart_type=chart_type,data_url=data_url,
                    options_dict=options_dict)
    else:
        return dict()


def plugin_return_data():
    """ CODE FOR SCRUM LITE IN THIS FUNCTION BELOW """
    sprint = db((db.Sprint.team_id==db.Team.id) & (db.Team.team_group==auth.user_groups.keys()[0])
    & (db.Sprint.start_date < request.now) & (db.Sprint.end_date > request.now)).select(db.Sprint.ALL).first()
    stories = db(sprint.id==db.Story.sprint_id).select(db.Story.ALL)

    start_date = sprint.start_date
    end_date = sprint.end_date
    today = datetime.datetime.now().date()

    total_pts = 0
    for story in stories:
        total_pts = total_pts + story.story_pts

    pts_compl = 0
    for story in stories:
        if story.completed is True:
            pts_compl = pts_compl+story.story_pts
    
    pts_left = total_pts - pts_compl
    
    total_days = str(end_date-start_date).split(' ')[0]
    days_left = str(end_date-today).split(' ')[0]
    days_in = str(today - start_date).split(' ')[0]
    
    projected_today = 0
    if total_pts != 0:
      projected_today = ((total_pts/total_days)*days_in)

    required_pace = 0
    if pts_left!=0:
      required_pace = (pts_left/days_left)*(projected_today-pts_compl)

    #stories = 
    # ["start date", 0, 0],["today", total pts/2, pts completed]["end date",total pts, *how to calculate pts based on current pace*]
    data = [['Date','Projected','Accomplished'],[start_date,0,0],["TODAY",projected_today,pts_compl],[end_date,total_pts,required_pace]]
    return dict(data=data)


def plugin_usage_example():
    return dict()
