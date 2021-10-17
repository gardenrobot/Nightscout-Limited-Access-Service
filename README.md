# Nightscout Limited Access Service

This is a webapp that allows Nightscout users to grant temporary access to the instance. Inspired by Google Maps' location sharing feature.

## How it works

The webapp will prompt the user for an email address of the person to share access with and the amount of time to share. A token will be generated and emailed to the person. After the given time has passed, the token will be revoked.

## Requirements

You will need
- a Nightscout server
- a subject with the `admin` role (created in Nightscout's admin page)
- SMTP login info

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
