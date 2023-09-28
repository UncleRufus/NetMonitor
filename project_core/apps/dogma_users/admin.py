# Utils
from django.contrib import admin
from django.db.models import Prefetch
from django.utils.html import format_html
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http import HttpResponseRedirect
from django.contrib.auth.admin import UserAdmin

# Modesl
from .models import DogmaUser, DogmaEmployee
from apps.dogma_infoseq.models import InfoSeqUserCertficateModel

# Forms
from .forms import DogmaUserCreateForm, DogmaUserCdhangeForm

# TypeHints
from django.http import HttpRequest
from typing import Sequence


@admin.register(DogmaUser)
class DogmaUserAdmiModel(UserAdmin):
    """Dogma user admin model"""

    add_form = DogmaUserCreateForm
    form = DogmaUserCdhangeForm

    def save_model(self, request: HttpRequest, obj: DogmaUser, form: any, change: bool) -> None:
        obj.is_staff = True
        obj.save()


@admin.register(DogmaEmployee)
class DogmaEmployeeAdminModel(admin.ModelAdmin):
    """"""

    """
    TODO Admin Employee:
    1) Добавить кнопку выпуска / перевыпуска сертификата
    2) Прикрутить LDAP запрос для пользователя
    3) Оптимизировать запрос в БД!!!
    """

    change_list_template: str = 'admin/employee_list_view.html'

    list_display: Sequence = (
        'short_name',
        'cert_status',
        'certificate_lifetime',
    )

    search_fields: Sequence = (
        'last_name',
    )

    actions: Sequence = (
        'make_published',
    )

    @admin.action(description="Отозвать сетрификат")
    def make_published(modeladmin, request, queryset):
        queryset.update(status="p")

    @admin.display(description='Сотрудник')
    def short_name(slef, obj: DogmaEmployee) -> str:
        """"""
        return obj.get_employee_short_name()

    @admin.display(description='Сертификат')
    def cert_status(self, obj: DogmaEmployee) -> str:
        """Return employee current certificate status"""

        try:
            employee_current_certificate = obj.vpn_certificate.filter(is_active=True).last()
            return format_html(
                f'<a href="{employee_current_certificate.get_admin_url()}" type="button">{employee_current_certificate.title}</a> |\
                <a href="#" type="button">Отозвать сертификат</a> |\
                <a href="#" type="button">Удалить сертификат</a>')

        except AttributeError:
            return format_html(f'<a href="#" type="button">Выпустить сертификат</a>')

    @admin.display(description='Сотрудник')
    def certificate_lifetime(slef, obj: DogmaEmployee) -> str:
        """"""

        try:
            employee_current_certificate: str = obj.vpn_certificate.filter(is_active=True).last()
            return employee_current_certificate.create_at.date()

        except AttributeError:
            return format_html(f'<a href="#" type="button">---</a>')

    def get_queryset(self, request: HttpRequest) -> QuerySet[any]:
        """"""

        qs = super().get_queryset(request)
        # return qs
        return qs.prefetch_related(Prefetch('vpn_certificate', queryset=InfoSeqUserCertficateModel.objects.select_related('employee').filter(is_active=True)))
