# Utils
import json
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

# Project settings
from web_core.settings import (
    DISCORD_ADMINISTROTUMSERVITOR,
    DISCORD_1LINE_SERVITOR,
    DISCORD_ASTRONOMIKON_SERVITOR,
    DISCORD_WARP_SERVITOR,
    )


# DTO
from utils.dto import DiscordOptionsDTO


class DiscordSenderManager:
    """Base discord notification send controller"""

    """
    TODO:
    1) Подготовить перенос в модуль notification_center
    """

    @classmethod
    def _manager(cls, event_author: str, event_type: str, event_field: str, event_value: str, event_content: DiscordOptionsDTO, servitor: str) -> None:
        """"""

        # --==COLOR TABLE==--
        # f84903 -> RED
        # 03b2f8 -> BLUE
        # 38761d -> GREEN

        match event_type:
            case 'test':
                cls.discord_sender(event_author=event_author, event_content=event_content, event_field=event_field, event_value=event_value, servitor=servitor, color='03b2f8')

            case 'Done':
                cls.discord_sender(event_author=event_author, event_content=event_content, event_field=event_field, event_value=event_value, servitor=servitor, color='38761d')

            case 'Error':
                cls.discord_sender(event_author=event_author, event_content=event_content, event_field=event_field, event_value=event_value, servitor=servitor, color='f84903')

        return 'SEND OK'

    @classmethod
    def discord_sender(cls, event_author: str, event_content: dict[str: any], event_field: str, event_value: str, servitor: str, color: str) -> None:
        """Send embed to discord"""

        tmp_event = json.loads(event_content)[0]

        webhook = DiscordWebhook(url=servitor)
        embed = DiscordEmbed(title=tmp_event.get('fields').get('title'), color=color)
        embed.set_author(name=event_author)
        embed.add_embed_field(name=event_field, value=event_value)
        embed.set_footer(text=tmp_event.get('fields').get('create_at'))
        webhook.add_embed(embed)
        webhook.execute()


class NotificationSendManager:
    """Notification send manager"""

    @classmethod
    def _manager(cls, notification_chanal: str, event_dto: str) -> None:
        """"""

        match notification_chanal:

            case 'Discord':
                cls.discord_sender(event_body=event_dto)

            case 'Telegram':
                cls.telegram_sender(event_body=event_dto)

            case 'Mail':
                cls.mail_sender(event_body=event_dto)

            case 'Bitrix':
                cls.bitrix_sender(event_body=event_dto)

        return 'SEND OK'

    @classmethod
    def discord_sender(cls, event_body: dict[str: any]) -> None:
        """Discord webhook sender"""

        event_color: str = '38761d'
        servitor: str = DISCORD_1LINE_SERVITOR

        if event_body.event_type == 'error':
            event_color: str = 'f84903'
            servitor: str = DISCORD_WARP_SERVITOR

        webhook = DiscordWebhook(url=servitor)
        embed = DiscordEmbed(title=event_body.event_content, color=event_color)
        embed.set_author(name=event_body.event_author)
        embed.add_embed_field(name=event_body.event_field, value=event_body.event_value)
        embed.set_footer(text=event_body.event_footer)
        webhook.add_embed(embed)
        webhook.execute()

    @classmethod
    def telegram_sender(cls, event_body: dict[str: any]) -> None:
        """"""
        pass

    @classmethod
    def mail_sender(cls, event_body: dict[str: any]) -> None:
        """"""
        pass

    @classmethod
    def bitrix_sender(cls, event_body: dict[str: any]) -> None:
        """"""
        pass
