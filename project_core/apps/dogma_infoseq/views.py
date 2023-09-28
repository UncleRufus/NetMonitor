# Utils
import requests
from django.shortcuts import render
from django.views.generic import View

# Decorators
from django.contrib.auth.decorators import login_required

# Project repo
from repository.notification_center import NotificationSendManager

# DTO
from utils.dto import DiscordNotificationDTO


"""
TODO:
    1) Переписать в класс
"""


class GetBitrixJson(View):
    """"""

    def get(self, request, *args, **kwargs):
        """"""
        pass


# @login_required
def sigur_request(request):
    """Return turnstiles_list"""

    tmp_dto = DiscordNotificationDTO(
        event_type = 'ok',
        event_author = 'Имя сервиса отправителя (VPN)',
        event_field = 'Тип события (Сертификат)',
        event_value = 'Статус события (Создан)',
        event_content = 'Какой-то контент (имя сертификата)',
        event_footer = 'Дата события',
    )

    if request.method == 'GET':
        local_request = requests.get('http://192.168.3.1:9090')
        # NotificationSendManager._manager(notification_chanal='Discord', event_dto=tmp_dto)

    context = {
        'sigur_data_list': local_request.json(),
        'sigur_data_length': len(local_request.json()),
    }
    template = 'visits/visits.html'
    return render(request, template, context)
