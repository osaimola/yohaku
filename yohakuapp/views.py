import math
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from yohakuapp.forms import TweetForm
from yohakuapp.models import Tweet, Identity

import os

import tweepy as tweepy

# Create your views here.

# pull api keys from heroku
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']


def setTwitterAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def makeTweet(api, tweet):
    # TODO add code to create real twitter threads for tweets greater than 280 chars
    api.update_status(tweet)


def index(request):
    context = {}
    if request.method == 'POST':
        form = TweetForm(request.POST)

        if form.is_valid():
            pending_tweet = form.save(commit=False)
            pending_tweet.date_created = timezone.now()

            # handle cases where tweets are longer than standard 280 characters
            api = setTwitterAuth()
            if len(pending_tweet.tweet_content) > 280:
                tweet_text = pending_tweet.tweet_content
                a = 0
                b = 272
                c = math.ceil((len(tweet_text)) / 272)
                for z in range(c):
                    makeTweet(api, (tweet_text[a:b] + " [" + str(z + 1) + "/" + str(c) + "]"))
                    a += 272
                    b += 272
                    time.sleep(1)
            else:
                makeTweet(api, pending_tweet.tweet_content)

            pending_tweet.publish_status = True

            # store an anonymous identifier in request.session
            anonymize(request=request, pending_tweet=pending_tweet)

            pending_tweet.save()
            return HttpResponseRedirect(reverse('yohakuapp:index'))
        else:
            print(form.errors)

    else:
        form = TweetForm()

    context['form'] = form
    list_of_tweets = Tweet.objects.all().order_by('-date_created')
    context['list_of_tweets'] = list_of_tweets
    return render(request, 'yohakuapp/index.html', context)


def anonymize(request, pending_tweet):
    """use sessions to set or retrieve an anonymous tag"""
    anonymous_id = request.session.get('anonymous_id', False)
    if anonymous_id:
        pending_tweet.user_id = int(anonymous_id)
    else:
        identifier = Identity.objects.get(pk=1)
        new_id = identifier.get_new_id()
        request.session['anonymous_id'] = new_id
        request.session.save()
        pending_tweet.user_id = new_id
