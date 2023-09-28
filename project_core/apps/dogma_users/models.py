# Django DB
from django.db import models
from django.urls import reverse

# Project Utils
from django.contrib.auth.models import AbstractUser
from .manager import DogmaUserManager

# Models
# from apps.dogma_infoseq.models import InfoSeqUserCertficateModel

# DTO
from utils.dto import DogmaEmployeeDTO


class DogmaUser(AbstractUser):
    """Basse DOGMA user model"""

    email = models.EmailField('Почта', db_index=True, unique=True)
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)

    objects = DogmaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self) -> str:
        return self.email


class DogmaEmployee(models.Model):
    """Base DOGMA employee model"""

    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255)
    email= models.EmailField('Почта', unique=True, db_index=True)

    department = models.CharField('Подразделение', max_length=255)
    position = models.CharField('Должность', max_length=255)

    # certificate = models.ForeignKey(InfoSeqUserCertficateModel, related_name='employee', verbose_name='Сертификат', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name: str = 'Сотрудник'
        verbose_name_plural: str = 'Сотрудники'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_admin_url(self):
        """"""
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])

    def get_employee_short_name(self):
        """Return formatted short name for employee"""
        return f'{self.last_name} {self.first_name[0].upper()}. {self.patronymic[0].upper()}.'

    def get_dto(self):
        """Return employee DTO"""

        own_certificate = self.vpn_certificate.filter(is_active=True).last()
        # own_certificate = 'None'

        return DogmaEmployeeDTO(
            first_name = self.first_name,
            last_name = self.last_name,
            patronymic = self.patronymic,
            email = self.email,
            depatment = self.department,
            position = self.position,
            current_certificate = own_certificate,
        )
