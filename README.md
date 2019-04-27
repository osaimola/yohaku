# yohaku

Django web app using the twitter api to send anonymous posts to a twitter handle ([@yooohaku](https://twitter.com/yooohaku))

See live demo on [yooohaku.herokuapp.com](http://yooohaku.herokuapp.com)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python

Django

This app uses the twitter APIs. So you will need to create twitter developer account and get a consumer key, consumer secret, access token and access secret.

You will also need to install the tweepy library

### Installing

Copy the yohaku folder to your machine.

Open yohaku\yohakuapp\views.py and replace the CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET with your keys. (the app will be unable to post to twitter without these)

Set Debug = True in yohaku\yohaku\settings.py to get detailed error messages.

Open the command line

cd to the yohaku folder

Get the app running with the following command

```
python manage.py runserver
```

You can now access yohaku at 127.0.0.1:8000
