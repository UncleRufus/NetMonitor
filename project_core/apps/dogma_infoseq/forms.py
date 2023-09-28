# Utils
from django.contrib import admin
from django import forms

# Models
from .models import InfoSeqUserCertficateModel, InfoSeqVPNRouteModel


class CreateNewCertificateForm(forms.ModelForm):
    """Форма для создания нового сертификата"""

    last_name = forms.CharField()
    first_name = forms.CharField()
    patronymic = forms.CharField()

    class Meta:
        model = InfoSeqUserCertficateModel
        fields = [
            'last_name',
            'first_name',
            'patronymic',
        ]


class ChangeCertficateForm(forms.ModelForm):
    """Форма для редактирования существующего сертификата"""

    class Meta:
        model = InfoSeqUserCertficateModel
        fields = [
            'employee',
            'country',
            'state',
            'locality',
            'organization',
            'unit',
            'key_size',
            'key_usage',
            'route',
            'password1',
            'password2',
            'destination',
            'is_active',
            'repeated',
        ]


class CreateVPNServiceForm(forms.ModelForm):
    """Base VPN Service create form"""

    class Meta:
        model = InfoSeqVPNRouteModel
        fields = [
            'title',
            'description',
            'route',
        ]


class EditVPNServiceForm(forms.ModelForm):
    """Base VPN Service edit form"""

    class Meta:
        model = InfoSeqVPNRouteModel
        fields = [
            'title',
            'description',
            'route',
            'slug',
        ]
