# Use an official Python runtime as a parent image
FROM python:3.8.9
# Set the working directory
WORKDIR /syncheck

RUN apt-get update && apt-get install -y apt-utils

RUN pip3 install gunicorn

# Copy the current directory contents into the container
COPY . /syncheck
RUN pip3 install -r requirements.txt -e .

#CMD [ "python3.6", "app.py" ]