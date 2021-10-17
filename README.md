# Nightscout Limited Access Service

This is a webapp that allows [Nightscout](https://github.com/nightscout/cgm-remote-monitor) users to grant people temporary access to the server. Inspired by Google Maps' location sharing feature.

## How it works

The webapp will prompt the user for an email address of the person to share access with, as well as the amount of time they will ahve access. It will generate a token and email it to the person. After the given time has passed, the app will revoke the token.

## Requirements

You will need
- a [Nightscout server](https://github.com/nightscout/cgm-remote-monitor)
- a subject with the `admin` role (created in Nightscout's admin page)
- SMTP login info (look up how to get this from your email provider)

## Future plans

I want to eventually have a way to limit the bg values that can be seen by a temporary user to only values in their time frame. In other words, someone that has been given access from 1pm-3pm should only be able to see values from 1pm-3pm.

## Installation (without Docker)

1. Check out the repo.

1. Install the Python requirements.

   `virtualenv -p python3 venv && source venv/bin/active && pip install -r requirements.txt`

1. Create `config.yml`.

   `cp config.yml.original config.yml`

1. Open it and fill in the needed data for the smtp, nightscout, and login sections.

1. Start it up.

   `source venv/bin/activate && python run.py`

## Installation (with Docker)

1. Check out the repo.

1. Create `config.yml`.

   `cp config.yml.original config.yml`

1. Open it and fill in the needed data for the smtp, nightscout, and login sections.

1. Build the image.

   `docker-compose build`

1. Start it up.

   `docker-compose up -d`
