from app import app, helper
from config import config
from flask import request, render_template, session, flash

@app.route('/')
def main():
    if not session.get('logged_in'):
        return render_template('login.html')

    return render_template('start.html')

@app.post('/share')
def share():
    if not session.get('logged_in'):
        return render_template('login.html')

    email = request.form['email']
    hours = int(request.form['hours'])

    # create subject
    subject_id = helper.create_subject(email, hours)

    # get token from id
    token = helper.get_token_from_subject_id(subject_id)

    # mail subject link to site
    helper.send_mail(email, hours, token)

    return render_template('share.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == config['login']['password'] and request.form['username'] == config['login']['username']:
        session['logged_in'] = True
    return main()
