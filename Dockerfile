# Use an official Python runtime as a parent image
FROM python:3.7

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV TWITCH_OAUTH_TOKEN TOKEN
ENV BOT_NAME blortbot
ENV BOT_CHANNEL beginbot

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

RUN useradd blortbot
RUN chown -R blortbot /code
RUN mkdir -p /home/blortbot
RUN chown -R blortbot /home/blortbot
USER blortbot

CMD exec python blortbot.py
