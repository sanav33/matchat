# syntax=docker/dockerfile:1

FROM python:3.9-buster

WORKDIR /matchat-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get -y install cron

ENV SLACK_API_URL="https://slack.com"
ENV ATLAS_CONNECTION_STR="mongodb+srv://admin:admin@matchatcluster.mixvt.mongodb.net/?retryWrites=true&w=majority"

COPY . /matchat-app

### CREATING CRON JOB
# Copy hello-cron file to the cron.d directory
COPY ./jobs/match /etc/cron.d/match
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/match
# Apply cron job
RUN crontab /etc/cron.d/match
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Start cron daemon
# RUN /etc/init.d/cron start
# ENTRYPOINT ["/etc/init.d/cron", "start"]

# EXPOSE 5000
# EXPOSE 8000

# ENTRYPOINT ["python3"]
# CMD ["main.py"]

# CMD ["gunicorn", "--bind 0.0.0.0:5000", "main:app"]
# CMD gunicorn main:app 0.0.0.0:5000
# CMD gunicorn main:app
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "main:app"]


# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]