# syntax=docker/dockerfile:1

FROM python:3.9-buster

WORKDIR /matchat-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get -y install cron

ENV SLACK_API_URL="https://slack.com"
ENV ATLAS_CONNECTION_STR="mongodb+srv://admin:admin@matchatcluster.mixvt.mongodb.net/?retryWrites=true&w=majority"

COPY . /matchat-app


# Copy hello-cron file to the cron.d directory
COPY ./jobs/match /etc/cron.d/match
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/match

# Apply cron job
RUN crontab /etc/cron.d/match
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
 
# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]