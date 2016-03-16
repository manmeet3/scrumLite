from gluon.serializers import json
from gluon.contrib.comet_messaging import comet_send
import urllib
import urllib2
import json
import chats

def index():
    team = 0
    form = 0
    forms = 0
    images = 0
    messages = ""
    if auth.is_logged_in():
        images = db(db.images.user==auth.user_id).select()
        if images:
            images = db(db.images.user==auth.user_id).select()[0]
            if not images:
                form = SQLFORM.factory(db.images,table_name='images')
                if form.process().accepted:
                    images = db.images.insert(image=form.vars.image, user=auth.user_id)
                    redirect(URL('index'))
        else:
            form = SQLFORM.factory(db.images,table_name='images')
            if form.process().accepted:
                images = db.images.insert(image=form.vars.image, user=auth.user_id)
                redirect(URL('index'))
        #code for chat start
        forms = SQLFORM(Post, formstyle = 'divs')
        if forms.process().accepted:
            #send messages on queue
            js = "jQuery('.new').slideDown('slow')"
            comet_send('http://127.0.0.1:8888', js, 'mykey', 'mygroup')
        messages = db(Post).select(orderby=~Post.created_on)
        #code for chat end

        groupid = 0
        if auth.user_groups.keys():
            groupid = auth.user_groups.keys()[0]
            team = db(db.Team.team_group == groupid).select().first()
        else:
            team=None
    else:
        first_name = ""
        last_name = ""
        identifier = ""
        email = ""
        password = "password"
        response.headers['content-type'] = 'text/xml'
        xml = request.body.read()  # retrieve the raw POST data
        token = xml[6:]
        print token
        if len(xml) == 0:
            xml = '<?xml version="1.0" encoding="utf-8" ?><root>no post data</root>'
        else:
            api_params = {
                'token': token,
                'apiKey': '73dab71b7fdfc0f49c10f8e64ee6a5adcf66b2c3',
                'format': 'json',
            }

            # make the api call
            http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
                                urllib.urlencode(api_params))

            # read the json response
            auth_info_json = http_response.read()

            # Step 3) process the json response
            auth_info = json.loads(auth_info_json)

            # Step 4) use the response to sign the user in
            if auth_info['stat'] == 'ok':
                profile = auth_info['profile']

                # 'identifier' will always be in the payload
                # this is the unique idenfifier that we use to sign the user
                # in to our site
                identifier = profile['identifier']
                first_name = profile["name"]["givenName"]
                last_name = profile["name"]["familyName"]
            else:
                 print 'An error occured: ' + auth_info['err']['msg']
        #checking if the user is already in the database
        users = db().select(db.auth_user.ALL)
        if users:
            users = db(db.auth_user.registration_id==identifier).select()
            if users:
                users = db(db.auth_user.registration_id==identifier).select()[0]
        if users:
            login = auth.login_bare(users.email,password)
            if (not login) & (auth_info['stat'] == 'ok'):
                db.auth_user.insert(
                first_name=first_name,
                last_name=last_name,
                registration_id=identifier,
                password=(db.auth_user.password.validate(password)[0]))
                login_again = auth.login_bare(email,password)
        else:
            print'Not able to login!'
    return dict(images=images,form=form,forms=forms,messages=messages,team=team)
def user():
    return dict(form=auth())

def show_sprint():
  if auth.user_groups.keys():
      sprint = db((db.Sprint.team_id==db.Team.id) & (db.Team.team_group==auth.user_groups.keys()[0])
      & (db.Sprint.start_date < request.now) & (db.Sprint.end_date > request.now)).select(db.Sprint.ALL).first()
      try:
          sprint.id
      except AttributeError:
          msg = 'No active Sprints found for your team'
          message = dict(msg=msg)
          return response.render('default/throw_error.html', message)
      else:
          stories = db(sprint.id==db.Story.sprint_id).select(db.Story.ALL)
          tasks = db((sprint.id==db.Story.sprint_id) & (db.Task.story_id==db.Story.id)).select(db.Task.ALL)
          backlogs = db((db.Story.team_id==auth.user_groups.keys()[0]) & (db.Story.backlogged==True)).select(db.Story.ALL)
          return dict(stories=stories, tasks=tasks, sprint=sprint, backlogs=backlogs)
  else:
      msg = 'you need to CREATE/JOIN a Team'
      return response.render('default/throw_error.html', dict(msg=msg))

def download():
    return response.download(request, db)
