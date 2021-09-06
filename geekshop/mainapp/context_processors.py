from authapp.models import ShopUserProfile
from basketapp.models import Basket


def basket(request):

    basket = []

    if request.user.is_authenticated:
        # basket = Basket.objects.filter(user=request.user)
        basket = request.user.basket.select_related()

    return {
        'basket': basket,
    }


def user_avatar(request):
    """
    Получить путь до пользовательского аватара
    :param request: объект запроса
    :return: словарь
    """
    avatar = {}

    if request.user.is_authenticated:

        if request.user.avatar:
            avatar = f'/media/{request.user.avatar}'

        else:
            user_profile = ShopUserProfile.objects.get(user=request.user)

            if user_profile.vk_user_avatar:
                avatar = user_profile.vk_user_avatar

        return {'avatar': avatar}

    return avatar
