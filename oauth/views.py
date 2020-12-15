from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from authlib.integrations.django_client import OAuth

oauth = OAuth()
oauth.register(name="github")
google = oauth.register(
    name='google',
    client_id='77533788752-8vdcs38vtcud4ghcsf52mt3jq0lr13e8.apps.googleusercontent.com',
    client_secret='runpXA5T3SHXTXLucH2AbxYd',
    access_token_url='https://www.googleapis.com/oauth2/v3/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',

    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info

    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/user.gender.read https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar'},
)

USERINFO_FIELDS = [
    'id', 'name', 'first_name', 'middle_name', 'last_name',
    'email', 'website', 'gender', 'locale'
]
USERINFO_ENDPOINT = 'me?fields=' + ','.join(USERINFO_FIELDS)


def normalize_userinfo(client, data):
    return map_profile_fields(data, {
        'sub': lambda o: str(o['id']),
        'name': 'name',
        'given_name': 'first_name',
        'family_name': 'last_name',
        'middle_name': 'middle_name',
        'email': 'email',
        'website': 'website',
        'gender': 'gender',
        'locale': 'locale'
    })


facebook = oauth.register(
    name="facebook",
    client_id="231440956951537",
    client_secret="34b980a4b7190adb4ced2daa3d95edfa",
    access_token_url='https://graph.facebook.com/v7.0/oauth/access_token',
    access_token_params=None,
    authorize_url='https://www.facebook.com/v7.0/dialog/oauth',
    authorize_params=None,
    api_base_url='https://graph.facebook.com/v7.0/',
    client_kwargs= {'scope': 'email public_profile user_birthday'},
    userinfo_endpoint = USERINFO_ENDPOINT,
    userinfo_compliance_fix = normalize_userinfo,
)


def index(request):
    breakpoint()
    redirect_uri = request.build_absolute_uri('/')
    return facebook.authorize_redirect(request, 'http://localhost:8000/complete')


def complete(request):
    breakpoint()

    token = oauth.facebook.authorize_access_token(request)

    resp = oauth.google.get('userinfo', token=token)
    return None 

# people apiを使う場合はpeople apiをenabledにして奥
# oauth.google.get('https://people.googleapis.com/v1/people/108294097194184170082?personFields=birthdays,genders', token=token)

