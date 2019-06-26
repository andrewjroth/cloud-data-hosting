#!/bin/sh
gunicorn --reload --access-logfile - --error-logfile - main:app