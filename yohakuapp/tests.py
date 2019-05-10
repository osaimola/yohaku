from django.test import TestCase
from django.urls import reverse
from yohakuapp.models import Tweet, Identity
from yohakuapp.forms import TweetForm
from yohakuapp.views import anonymize
import random
import string
from django.utils import timezone


# Create your tests here.
def create_tweet(tweet_content, publish_status=False, user_id=0):
    """creates a new tweet object"""
    return Tweet.objects.create(tweet_content=tweet_content, date_created=timezone.now(), publish_status=publish_status,
                                user_id=user_id)


def create_identity():
    return Identity.objects.create()


def create_string(length):
    """creates a random string with given lenght"""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


class TweetFormTest(TestCase):

    def test_valid_data(self):
        """form should accept and process valid data"""
        text = create_string(200)
        form = TweetForm({
            'tweet_content': text
        })
        self.assertTrue(form.is_valid())
        tweet = form.save(commit=False)
        tweet.date_created = timezone.now()
        tweet.save()
        self.assertEqual(tweet.tweet_content, text)
        self.assertEqual(tweet.tweet_intro, text[:30])

    def test_blank_data(self):
        """empty data should not be valid"""
        form = TweetForm({})
        self.assertFalse(form.is_valid())


class TweetModelTest(TestCase):

    def test_tweet_intro_with_short_tweet(self):
        """tweet_content should"""
        text = create_string(15)
        tweet = create_tweet(tweet_content=text)
        self.assertEqual(tweet.tweet_intro, text)

    def test_tweet_intro_with_long_tweet(self):
        """tweet_intro should be created from first 30 characters of tweet_content"""
        text = create_string(300)
        tweet = create_tweet(tweet_content=text)
        self.assertEqual(tweet.tweet_intro, text[:30])


class IdentityModelTest(TestCase):

    def test_default_id_count(self):
        """Identity object should have default ID of 1"""
        id = create_identity()
        self.assertEqual(id.id_count, 1)

    def test_get_new_id(self):
        """get_new_id() should return the current id count and increase the count by +1"""
        id = create_identity()
        self.assertEqual(id.id_count, 1)
        a = id.get_new_id()
        b = id.get_new_id()
        c = id.get_new_id()
        self.assertEqual((a, b, c), (1, 2, 3))


class TweetIndexViewTest(TestCase):

    def test_no_tweets(self):
        """if no tweets exist, a message indicates this"""
        response = self.client.get(reverse('yohakuapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['list_of_tweets'], [])
        self.assertContains(response, "No thoughts shared yet..")

    def test_single_tweet(self):
        """the index page should display created tweets"""
        text = create_string(240)
        tweet = create_tweet(tweet_content=text)
        response = self.client.get(reverse('yohakuapp:index'))
        self.assertQuerysetEqual(response.context['list_of_tweets'], ['<Tweet: ' + text[:30] + '>'])

    def test_reverse_chronological_order(self):
        """the index page should display all created tweets with most recent tweets first"""
        text = create_string(240)
        create_tweet(tweet_content=text)
        text2 = create_string(680)
        create_tweet(tweet_content=text2)
        text3 = create_string(1020)
        create_tweet(tweet_content=text3)
        response = self.client.get(reverse('yohakuapp:index'))
        self.assertQuerysetEqual(response.context['list_of_tweets'],
                                 ['<Tweet: ' + text3[:30] + '>', '<Tweet: ' + text2[:30] + '>',
                                  '<Tweet: ' + text[:30] + '>'])

    def test_anonymize(self):
        """anonymize should assign an anonymous ID to tweets"""
        create_identity()
        text = create_string(340)
        form = TweetForm({
            'tweet_content': text
        })
        tweet = form.save(commit=False)
        # use self.client to represent the request. this will then hold the session value
        request = self.client
        request.get('/')
        anonymize(session=request.session, pending_tweet=tweet)
        tweet.date_created = timezone.now()
        tweet.save()
        self.assertEqual(tweet.user_id, 1)

    def test_anonymize_with_multiple_users(self):
        """anonymize should assign a different anonymous ID to tweets from different users"""
        create_identity()

        # create the requests and sessions
        request = self.client
        session = request.session
        request.get('/')

        # create first tweet
        text = create_string(340)
        form = TweetForm({
            'tweet_content': text
        })
        tweet = form.save(commit=False)
        anonymize(session=request.session, pending_tweet=tweet)
        # saving session will create a new session on next request.session call ?????
        session.save()
        tweet.date_created = timezone.now()
        tweet.save()

        # create second tweet
        text2 = create_string(720)
        form2 = TweetForm({
            'tweet_content': text2
        })
        tweet2 = form2.save(commit=False)
        anonymize(session=request.session, pending_tweet=tweet2)
        tweet2.date_created = timezone.now()
        tweet2.save()

        self.assertEqual((tweet.user_id, tweet2.user_id), (1, 2))

    def test_anonymize_with_single_user(self):
        """anonymize should assign the same anonymous ID to all tweets from a single user"""
        create_identity()

        # use session = request.session hold the SINGLE REQUEST needed. this will prevent creation of a new session
        request = self.client
        session = request.session
        request.get('/')

        # create first tweet
        text = create_string(340)
        form = TweetForm({
            'tweet_content': text
        })
        tweet = form.save(commit=False)
        anonymize(session=session, pending_tweet=tweet)
        tweet.date_created = timezone.now()
        tweet.save()

        # create second tweet
        text2 = create_string(720)
        form2 = TweetForm({
            'tweet_content': text2
        })
        tweet2 = form2.save(commit=False)
        anonymize(session=session, pending_tweet=tweet2)
        tweet2.date_created = timezone.now()
        tweet2.save()

        self.assertEqual((tweet.user_id, tweet2.user_id), (1, 1))
