from datetime import datetime, timedelta
from email.message import EmailMessage
from smtplib import SMTP_SSL
from config import config
import re
import requests
import time

ROLES = ['admin', 'readable'] # Readable is redundant. There is some issue with only sending one item in the list. TODO fix this.

SUBJECT_PREFIX = 'NLAS Temp'

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def send_mail(email, hours, token):
    """
        Takes an email address, number of hours, and the generation auth token.
        Connects to the SMTP and sends email.
    """
    smtp_config = config['smtp']
    url = config['nightscout']['url']

    msg = EmailMessage()
    body = 'You have been given access to a Nightscout instance.\nSite: {}?token={}\nTime: {} hour(s)'.format(url, token, hours)
    msg.set_content(body)
    msg['Subject'] = 'Nightscout - You have been given temporary access'
    msg['From'] = smtp_config['address']
    msg['To'] = email

    with SMTP_SSL(smtp_config['server'], port=smtp_config['port']) as smtp:
        smtp.login(smtp_config['address'], smtp_config['password'])
        smtp.send_message(msg)

def get_token_from_subject_id(subject_id):
    return [s['accessToken'] for s in get_subjects() if s['_id'] == subject_id][0]

def get_subjects():
    """Returns a list of all subjects"""
    url = config['nightscout']['url']
    params = {'token': config['nightscout']['token']}

    r = requests.get(url, params=params)
    return r.json()

def create_subject(email, hours):
    """
        Takes an email address and number of hours and creates a subject that
        expires X hours from the current time. Returns the subject id.
    """
    url = config['nightscout']['url']
    params = {'token': config['nightscout']['token']}

    delete_time = (datetime.now() + timedelta(hours=hours)).strftime(DATE_FORMAT)
    data = {
        'name': '{}: {}; Expires {}'.format(SUBJECT_PREFIX, email, delete_time),
        'roles': ROLES,
    }
    res = requests.post(url, params=params, data=data)
    subject_id = res.json()[0]['_id']
    return subject_id

def delete_subject(subject_id):
    """Takes a subject id and deletes it from NS"""
    url = config['nightscout']['url']
    params = {'token': config['nightscout']['token']}

    delete_url = url+'/'+subject_id
    r = requests.delete(delete_url, params=params)

def delete_old_subjects():
    """
        Grabs the subjects from NS, checks if they have expired, and
        deletes the expired.
    """
    print('Running delete_old_subjects()')
    subjects = get_subjects()
    now = datetime.now()

    for subject in subjects:
        res = re.search(r'; Expires (.*)', subject['name'])
        if res:
            expiration = datetime.strptime(res.group(1), DATE_FORMAT)
            if expiration < now:
                delete_subject(subject['_id'])

def delete_loop():
    """Runs the loop to delete expired tokens on Nightscout."""
    while True:
        interval = config['delete_loop_interval']
        delete_old_subjects()
        time.sleep(interval)
