"""Twitter Login/Connect View."""
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from dj_rest_auth.social_serializers import (
    TwitterConnectSerializer,
    TwitterLoginSerializer,
)


class TwitterLoginView(SocialLoginView):
    """Twitter Login View definitions.

    sa: https://dj-rest-auth.readthedocs.io/en/latest/installation.html#twitter
    """

    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class TwitterConnectView(SocialConnectView):
    """Twitter Connect View definitions."""

    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter
