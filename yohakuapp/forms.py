from django import forms
from yohakuapp.models import Tweet, Identity


class TweetForm(forms.ModelForm):
    tweet_content = forms.CharField(help_text="What's on your mind?")

    class Meta:
        model = Tweet
        fields = ('tweet_content',)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        # this adds class="twitter-form" css tag for the specified form fields
        self.fields['tweet_content'].widget.attrs.update({'class': 'twitter-form'})
