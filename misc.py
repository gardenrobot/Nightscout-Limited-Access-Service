from smtplib import SMTP_SSL
from email.message import EmailMessage
import nightscout
import time
import yaml

def send_mail(email, hours, token):
    """
        Takes an email address, number of hours, and the generation auth token.
        Connects to the SMTP and sends email.
    """
    config = load_config()
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

def load_config():
    """Returns config.yaml as a dict"""
    with open('config.yml', 'r') as f:
        yml = yaml.safe_load(f)
    return yml

def delete_loop():
    """Runs the loop to delete expired tokens on Nightscout."""
    while True:
        interval = load_config()['delete_loop_interval']
        nightscout.delete_old_subjects()
        time.sleep(interval)
