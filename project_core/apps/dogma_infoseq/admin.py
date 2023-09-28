# Utils
import datetime
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.utils.html import format_html

from django.http.request import HttpRequest

# Models
from .models import (
    InfoSeqReportModel,
    InfoSeqVPNRouteModel,
    InfoSeqUserCertficateModel,
    )

# Forms
from .forms import CreateNewCertificateForm, ChangeCertficateForm, CreateVPNServiceForm

# Inlines
from .inlines import InfoSeqCDPAgentInline, InfoSeqLLDPAgentInline

# ProjectRepo
from repository.test import test_parser
from repository.report_center import ReportControlCenter, TraficMonitor
from repository.certification_center import CertificateControlCenter

# ProjectUtils
from utils.formatters import user_sertificate_name_formatter, user_password_generator

# TypeHints
from django.http import HttpRequest
from django.db.models import QuerySet
from typing import Any, Dict, Optional, Sequence, Tuple


@admin.register(InfoSeqReportModel)
class InfoSeqAdminModel(admin.ModelAdmin):
    """Base InfoSeq report class admin model view"""

    inlines: Sequence[str] = (
        InfoSeqCDPAgentInline,
        InfoSeqLLDPAgentInline,
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[any]:
        """"""

        qs = super().get_queryset(request)
        return qs.prefetch_related('cdp_report', 'lldp_report')


@admin.register(InfoSeqUserCertficateModel)
class UserCertficateAdminModel(admin.ModelAdmin):
    """Base Certificate admin view"""

    #form = CreateNewCertificateForm
    form = ChangeCertficateForm
    change_form_template = 'admin/certificate_change_form.html'

    list_filter: Sequence = (
        'is_active',
        'destination',
    )

    readonly_fields: Sequence = (
        'create_at',
    )

    list_display: Sequence = (
        'owner',
        'cert_detail',
        'cert_destination',
        'cert_life_time',
        'is_active',
        'manage_buttons',
    )

    search_fields: Sequence = (
        'employee__last_name',
    )

    @admin.display(description='Пользователь')
    def owner(self, obj: InfoSeqUserCertficateModel) -> str:
        """Return certificate owner short name"""

        try:
            cert_employee = obj.employee
            return format_html(f'<a href="{cert_employee.get_admin_url()}">{cert_employee.get_employee_short_name()}</a>')

        except AttributeError:
            return "None"

    @admin.display(description='Сертификат')
    def cert_detail(self, obj: InfoSeqUserCertficateModel) -> str:
        """Return certificate title"""

        return format_html(f'<a href="{obj.get_admin_url()}">{obj.title}</a>')

    @admin.display(description='Платформа')
    def cert_destination(self, obj: InfoSeqUserCertficateModel) -> str:
        """Return certificate owner short name"""
        return obj.destination.lower()

    @admin.display(description='Период активности')
    def cert_life_time(self, obj: InfoSeqUserCertficateModel) -> str:
        """Return estimated certificate validity period"""

        obj_create_date = obj.create_at.date()
        obj_end_date = obj_create_date + datetime.timedelta(days=365)
        validate_period = (obj_end_date - datetime.datetime.now().date())
        certificate_validity_period = f'C: {obj_create_date} | ПО: {obj_end_date} | Всего: ({validate_period.days} Дней)'
        return certificate_validity_period

    @admin.display(description='Срок действия')
    def cert_validity(self, obj: InfoSeqUserCertficateModel) -> int:
        """Return certificate validity in days"""

        end_date = obj.get_certificate_dto().created_at + datetime.timedelta(days=365)
        date = (end_date - datetime.datetime.now().date())
        return date.days

    @admin.display(description='Управление сертификатом')
    def manage_buttons(self, obj: InfoSeqUserCertficateModel) -> str:
        """Return certificate owner short name"""

        if obj.is_active:
            return format_html(f'<a href="#" type="button" class="default">Перевыпустить</a> |\
                                <a href="#" type="button" class="deletelink">Отозвать</a>')

        return format_html(f'<a href="#" type="button" class="addlink">Выпустить</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet[any]:
        """Return queryset certificates from DB"""

        qs = super().get_queryset(request).select_related('employee')
        return qs

    def save_model(self, request: HttpRequest, obj: InfoSeqUserCertficateModel, form: any, change: bool) -> None:
        """Save User Certficate Model"""

        # При создании нового сертификата
        if not obj.pk:
            print(request.POST)

            employee_cert_keypass: dict[str: str] = user_password_generator()
            employee_short_name: str = f'{obj.employee.last_name}_{obj.employee.first_name[0].lower()}'
            obj.password1 = employee_cert_keypass.key
            obj.password2 = employee_cert_keypass.passwd
            obj.title = f"{user_sertificate_name_formatter(employee_name=employee_short_name)}-{obj.destination.lower()}"
            obj.save()

            # Выпуск нового сертификата
            CertificateControlCenter._manager(certificate_pk=obj.pk)

        return super().save_model(request, obj, form, change)


@admin.register(InfoSeqVPNRouteModel)
class VPNRouteAdminModel(admin.ModelAdmin):
    """Base VPN Route admin view"""

    form = CreateVPNServiceForm

    list_display: Sequence = (
        'title',
        'route',
    )

    def save_model(self, request: HttpRequest, obj: InfoSeqVPNRouteModel, form: any, change: bool) -> None:
        """Save VPNRoute Model"""

        if not obj.pk:
            obj.slug = obj.route
            obj.save()

        return super().save_model(request, obj, form, change)

