from config import config
from flask import Flask, session
import _thread
import yaml


DEV_MODE=True

from app import app, helper

if __name__ == '__main__': # TODO turn debug mode off
    # Start the delete loop in its own thread
    _thread.start_new_thread(helper.delete_loop, ())

    # Start flask
    app.run(host='0.0.0.0', port=config['port'], debug=DEV_MODE) # TODO how to do prod mode?
