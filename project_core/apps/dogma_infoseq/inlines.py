# Utils
from django.contrib import admin

# Models
from .models import InfoSeqCDPAgentModel, InfoSeqLLDPAgentModel


class InfoSeqCDPAgentInline(admin.TabularInline):
    """CDPAgent Inline"""

    model: InfoSeqCDPAgentModel = InfoSeqCDPAgentModel
    verbose_name: str = 'CDP Отчет'
    verbose_name: str = 'CDP Отчеты'
    extra: int = 0
    show_change_link: bool = False


class InfoSeqLLDPAgentInline(admin.TabularInline):
    """LLDPAgent Inline"""

    model: InfoSeqLLDPAgentModel = InfoSeqLLDPAgentModel
    verbose_name: str = 'LLDP Отчет'
    verbose_name: str = 'LLDP Отчеты'
    extra: int = 0
    show_change_link: bool = False
