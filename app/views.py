from app import app, helper
from flask import request

@app.route('/') # TODO put html in template files
def main(): # TODO password protect this
    return '''
<html>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3pro.css">
  <form action="/share" method="POST">
    <label for="email">Email to share with:</label><br/>
    <input name="email" type="email"/><br/>
    <label for="hours">Hours to share for:</label><br/>
    <input name="hours" type="number"/><br/>
    <button type="submit">Share!</button>
  </form>
</html>'''

@app.post('/share')
def share():
    email = request.form['email']
    hours = int(request.form['hours'])

    # create subject
    subject_id = helper.create_subject(email, hours)

    # get token from id
    token = [s['accessToken'] for s in helper.get_subjects() if s['_id'] == subject_id][0]

    # mail subject link to site
#    helper.send_mail(email, hours, token)

    return '''
<html>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3pro.css">
  <div>Sent! A link to the Nightscout app has been sent to their email.</div>
</html>'''
