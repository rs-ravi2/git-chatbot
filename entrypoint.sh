#!/bin/bash

# Start the run once job.
echo "Docker container has been started"
#pip  install --trusted-host https://pypi.org python-crontab
cd /app/
uvicorn main:app --host 0.0.0.0 --log-level debug --use-colors