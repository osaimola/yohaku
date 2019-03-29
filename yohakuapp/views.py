from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from yohakuapp.forms import TweetForm
from yohakuapp.models import Tweet, Identity

from boto.s3.connection import S3Connection

import tweepy as tweepy

# Create your views here.
#TODO hide api key
s3 = S3Connection(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'], os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])


def setTwitterAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


def makeTweet(api, tweet):
    #TODO add code to create threads for tweets greater than 280 chars
    api.update_status(tweet)

def index(request):
    context ={}
    if request.method == 'POST':
        form = TweetForm(request.POST)

        if form.is_valid():
            pending_tweet = form.save(commit=False)

            #TODO handle tweets longer than 280 characters and update tweet model to reflect
            api = setTwitterAuth()
            makeTweet(api, pending_tweet.tweet_content)
            pending_tweet.publish_status=True

            #TODO update anonymous USERID and save to pending tweet
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
