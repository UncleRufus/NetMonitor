# Utils
from django.db import models
from django.urls import reverse

# Models
from apps.dogma_users.models import DogmaEmployee

# Choices
from utils.choices import (
    VPNCertificateDestination,
    VPNCertificateCountry,
    VPNCertificateKeySize,
    VPNCertificateKeyUsage,
    VPNCertificateOrganization,
    VPNCertificateState,
    VPNCertificateUnit,
    VPNCertificateLocality,
)

# DTO
from utils.dto import CertificateDTO


class InfoSeqReportModel(models.Model):
    """Base report model"""

    date = models.DateTimeField('Дата', auto_created=True)

    class Meta:
        verbose_name: str = 'Отчет'
        verbose_name_plural: str = 'Отчеты'

    def __str__(self) -> str:
        return self.date.date


class InfoSeqCDPAgentModel(models.Model):
    """CDP Agent model"""

    platform = models.CharField('Хост', max_length=255)
    model = models.CharField('Модель', max_length=255)
    ip_address = models.CharField('IP Адресс', max_length=255)
    port = models.SmallIntegerField('Порт', default=0)

    report = models.ForeignKey(InfoSeqReportModel, related_name='cdp_report', verbose_name='Отчет', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.platform

    class Meta:
        verbose_name: str = 'CDP Агент'
        verbose_name_plural: str = 'CDP Агенты'


class InfoSeqLLDPAgentModel(models.Model):
    """LLDP Agent model"""

    platform = models.CharField('Хост', max_length=255)
    model = models.CharField('Модель', max_length=255)
    ip_address = models.CharField('IP Адресс', max_length=255)
    port = models.SmallIntegerField('Порт', default=0)

    report = models.ForeignKey(InfoSeqReportModel, related_name='lldp_report', verbose_name='Отчет', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return self.platform

    class Meta:
        verbose_name: str = 'LLDP Агент'
        verbose_name_plural: str = 'LLDP Агенты'


class InfoSeqVPNRouteModel(models.Model):
    """Service route model"""

    title = models.CharField('Назване', max_length=255)
    description = models.TextField('Описание')
    route = models.CharField('Путь', max_length=255)
    slug = models.SlugField('Идентификатор', max_length=255, unique=True, db_index=True, blank=True)

    class Meta:
        verbose_name: str = 'Сервис'
        verbose_name_plural: str = 'ВПН Сервисы'

    def __str__(self) -> str:
        return f'{self.title} {self.route}'


class InfoSeqUserCertficateModel(models.Model):
    """User Certificate base model"""

    title = models.CharField('Сертификат', max_length=255, blank=True, null=True)
    password1 = models.CharField('Ключ сертификата', max_length=255, blank=True, null=True)
    password2 = models.CharField('РРР Пароль', max_length=255, blank=True, null=True)

    country = models.CharField(max_length=20, default=VPNCertificateCountry.RU, choices=VPNCertificateCountry.choices)
    state = models.SmallIntegerField(default=VPNCertificateState.krd, choices=VPNCertificateState.choices)
    organization = models.CharField(max_length=20, default=VPNCertificateOrganization.DOGMA, choices=VPNCertificateOrganization.choices)
    unit = models.CharField(max_length=20, default=VPNCertificateUnit.DIS, choices=VPNCertificateUnit.choices)
    key_size = models.CharField(max_length=20, default=VPNCertificateKeySize.LARGE, choices=VPNCertificateKeySize.choices)
    key_usage = models.CharField(max_length=20, default=VPNCertificateKeyUsage.TLS, choices=VPNCertificateKeyUsage.choices)
    locality = models.CharField(max_length=20, default=VPNCertificateLocality.KRD, choices=VPNCertificateLocality.choices)

    employee = models.ForeignKey(DogmaEmployee, related_name='vpn_certificate', verbose_name='Сотрудник', on_delete=models.CASCADE)
    route = models.ManyToManyField(InfoSeqVPNRouteModel, related_name='routs', verbose_name='Сервис', blank=True)

    destination = models.CharField(max_length=20, default=VPNCertificateDestination.WINDOWS, choices=VPNCertificateDestination.choices)

    create_at = models.DateTimeField('Дата выдачи', auto_now_add=True)
    is_active = models.BooleanField('Актуален', default=True)
    repeated = models.BooleanField('Повторный', default=False)

    class Meta:
        verbose_name: str = 'Сертификат'
        verbose_name_plural: str = 'Сертификаты'

    def __str__(self) -> str:
        return self.title

    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])

    def get_certificate_dto(self) -> CertificateDTO:
        """Return create certificate command DTO"""

        self_routs = [route.route for route in self.route.all()]
        self_create_at = self.create_at.date()
        self_employee = self.employee

        return CertificateDTO(
            title = self.title,
            country = self.country,
            state = self.state,
            locality = self.locality,
            organization = self.organization,
            unit = self.unit,
            common_name = self.title,
            key_size = self.key_size,
            routes = self_routs,
            key_usage = self.key_usage,
            employee = self_employee,
            cert_destination=self.destination,
            passwd = self.password1,
            key = self.password2,
            created_at=self_create_at,
            repeated = self.repeated,
        )
