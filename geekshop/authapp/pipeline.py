from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop.settings import SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_ACCESS_TOKEN, \
    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        print('ВК')
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join((
                                  'bdate',
                                  'sex',
                                  'about',
                                  'domain',
                                  'personal',
                                  'photo_100'
                              )),
                                  access_token=response['access_token'],
                                  v='5.131')), None
                              ))
        print(api_url)

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if data['domain']:
            user.shopuserprofile.vk_profile = f'https://vk.com/{data["domain"]}'

        if data['photo_100']:
            user.shopuserprofile.vk_user_avatar = f'{data["photo_100"]}'

        if len(data['personal']) > 0 and data['personal']['langs'] and len(data['personal']['langs']) > 0:
            user.shopuserprofile.language = data['personal']['langs'][0]

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                # При debug = True при исключении AuthForbidden перенаправляет на главную
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.save()

    if backend.name == 'odnoklassniki-oauth2':
        # Необходимо дописать функцию md5 для параметра sig
        api_url = f'https://api.ok.ru/fb.do?application_key={SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME}&format=json&method=users.getCurrentUser&sig=61536f08bd8ffaacfccea17ae6f06945&access_token={SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_ACCESS_TOKEN}'
        resp = requests.get(api_url)

        if resp.status_code != 200:
            return

        data = resp.json()

        if data['uid']:
            user.shopuserprofile.ok_profile = f'https://ok.ru/profile/{data["uid"]}'

        if data['gender']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['gender'] == 'male' else ShopUserProfile.FEMALE

        if data['pic_2']:
            user.shopuserprofile.vk_user_avatar = f'{data["pic_2"]}'

        if data['location']['countryCode']:
            user.shopuserprofile.language = data['location']['countryCode']

        user.save()

    else:
        return
