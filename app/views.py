from app import app, helper
from flask import request, render_template

@app.route('/') # TODO put html in template files
def main(): # TODO password protect this
    return render_template('start.html')

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

    return render_template('share.html')
