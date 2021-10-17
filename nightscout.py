from datetime import datetime, timedelta
import misc
import requests
import re

ROLES = ['admin', 'readable'] # Readable is redundant. There is some issue with only sending one item in the list. TODO fix this.

SUBJECT_PREFIX = 'NSSS Temp'

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_subjects():
    """Returns a list of all subjects"""
    config = misc.load_config()
    url = config['nightscout']['url']
    params = {'token': config['nightscout']['token']}

    r = requests.get(url, params=params)
    return r.json()

def create_subject(email, hours):
    """
        Takes an email address and number of hours and creates a subject that
        expires X hours from the current time. Returns the subject id.
    """
    config = misc.load_config()
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
    config = misc.load_config()
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

