# Utils
import subprocess
import datetime
from django.core import serializers
from jinja2 import Environment, FileSystemLoader

# ProjectSettings
from web_core.settings import INFOSEQ_ROOT, DISCORD_1LINE_SERVITOR, DISCORD_WARP_SERVITOR

# ProjectRepo
from repository.device_center import DeviceController
from repository.notification_center import DiscordSenderManager

# Models
from apps.dogma_infoseq.models import InfoSeqUserCertficateModel
from django.db.models import QuerySet

# DTO
from utils.dto import CertBlocksDTO, CertificateDTO


class CertificateControlCenter:
    """Certificate parser class"""

    """
    TODO:
    1. Проработать корретное извлечение роутов из сертификата;
    2. Проработать корретную запись в шаблон сертификата:
        * Добавить парсинг роутов в сертификат
    3. Проработать перевыпуск сертификата:
        * Добавить идентификатор в имя сертификата
        * Записать новый common_name сертификата в его DTO
    4. Проработать отправку уведомления пользователю за 5 дней до конца действия сертификата:
        * Проработать отправку уведомления по почте;
    4. Проработать удаление остаточных файлов:
        * *.ctr
        * *.p12
    5. ВСЕ ХУЙНЯ, НАДО ПЕРЕДЕАЛАТЬ!!!!
        * ИСХОДНЫЕ ДАННЫЕ ДЛЯ ПУТЕЙ И НАИМЕНОВАНИЙ БРАТЬ С РАСПАРСЕННОГО p12_certificate_path !!!!!!
    """

    """
    tmp_dto = DiscordNotificationDTO(
        event_type = 'ok',
        event_author = 'Имя сервиса отправителя (VPN)',
        event_field = 'Тип события (Сертификат)',
        event_value = 'Статус события (Создан)',
        event_content = 'Какой-то контент (имя сертификата)',
        event_footer = 'Дата события',
    )

    NotificationSendManager._manager(notification_chanal='Discord', event_dto=tmp_dto)
    """

    @classmethod
    def _manager(cls, certificate_pk: int) -> bool | Exception:
        """Certificate management"""

        current_certificate: InfoSeqUserCertficateModel = InfoSeqUserCertficateModel.objects.get(pk=certificate_pk)
        current_cert_dto: CertificateDTO = current_certificate.get_certificate_dto()
        serialized_current_certificate: list[dict[str: any]] = serializers.serialize('json', [current_certificate])

        p12_certificate_path: str = DeviceController._manager(command_type='create_vpn_certificate', certificate_dto=current_cert_dto)

        jinja_base_template_name: str = 'base_cert__template.txt'

        if p12_certificate_path.split('/')[-1].split('.')[0].split('-')[-1] == 'ipad':
            jinja_base_template_name: str = 'ipad_cert__template.txt'

        # else:

        try:
            # Конвертация сертификата с *.p12 в *.crt
            crt_certificate_path = cls.file_certificate_conversion(
                p12_certificate_path=p12_certificate_path,
                certificate_title=p12_certificate_path.split('/')[-1].split('.')[0],
                crt_certificate_password=current_cert_dto.passwd,
            )

            # Парсинг *.crt на блоки <cert> <ca> <key>
            certificate_block_dict: dict[str: any] = cls.crt_certificate_parser(
                crt_certificate_path=crt_certificate_path
            )

            # Извлечение роутов
            actual_routes: list[str] = cls.get_cretificate_routes(cert_routs=current_cert_dto)

            # Компановка блоков для формирования сертификата
            blocks_dict: dict[str: any] = {
                'cert_body': certificate_block_dict.cert_body,
                'ca_body': certificate_block_dict.ca_body,
                'key_body': certificate_block_dict.key_body,
                }

            # Подготовка шаблона для Jinja2
            certificate_template: str = cls.get_certifacate_template(
                template_name=jinja_base_template_name,
                blocks_dict=blocks_dict
            )

            # Создание *.ovpn сертификата
            cls.ovpn_certificate_create(
                cert_template=certificate_template,
                ovpn_certificate_name=current_cert_dto.title
            )

            # Удаление остаточных файлов
            # cetrificate_storage_path = f'{INFOSEQ_ROOT}/user_certificates'
            # cls.cert_template_cleaner(cetrificate_storage_path=cetrificate_storage_path)

            # Отправка оповещения в дискорд
            DiscordSenderManager._manager(
                event_author='VPN Центр',
                event_type='Done',
                event_field='Сертификат',
                event_value = 'V Создан V',
                event_content=serialized_current_certificate,
                servitor=DISCORD_1LINE_SERVITOR
            )

        except Exception as error:
            # Отправка оповещения в дискорд
            DiscordSenderManager._manager(
                event_author='VPN Центр',
                event_type='Error',
                event_field='Сертификат',
                event_value = 'Х Ошибка Х',
                event_content=serialized_current_certificate,
                servitor=DISCORD_WARP_SERVITOR
            )
            print(f'CertificateControlCenter -> Вернул {error}')

    @classmethod
    def file_certificate_conversion(cls, p12_certificate_path: str, certificate_title: str, crt_certificate_password: str):
        """Conversion certificate file from *.p12 to *.crt"""

        crt_certificate_path: str = f'{INFOSEQ_ROOT}/user_certificates/{certificate_title}.crt'

        create_cert = subprocess.run(
            f"openssl pkcs12 -in {p12_certificate_path} -nodes -out {crt_certificate_path} -passin pass:{crt_certificate_password}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            check=True
        )

        if create_cert.returncode != '0':
            return crt_certificate_path

        else:
            return ValueError(f'Конвертация сертификата на уровне ОС из *.p12 в *.crt вернула ошибку {create_cert.returncode}')

    @classmethod
    def crt_certificate_parser(cls, crt_certificate_path: str) -> CertBlocksDTO | Exception:
        """Delete info strings, parse certificate to blocks"""

        with open(crt_certificate_path, 'r') as cert_file:
            cert_arr = [item.strip() for item in cert_file.readlines()\
                        if not item.startswith('Bag Attributes')\
                        and not item.startswith('    localKeyID:')\
                        and not item.startswith('    friendlyName:')\
                        and not item.startswith('subject')\
                        and not item.startswith('issuer')\
                        and not item.startswith('Key Attributes:')]

        for cert_string in cert_arr:
            if cert_string.startswith('-----BEGIN CERTIFICATE-----'):
                ca_start_string_index = cert_arr.index(cert_string)

            elif cert_string.startswith('-----END CERTIFICATE-----'):
                ca_end_string_index = cert_arr.index(cert_string)

            elif cert_string.startswith('-----BEGIN PRIVATE KEY-----'):
                key_start_string_index = cert_arr.index(cert_string)

            elif cert_string.startswith('-----END PRIVATE KEY-----'):
                key_end_string_index = cert_arr.index(cert_string)

        ca_body: list[str] = [item for item in cert_arr[ca_start_string_index:ca_end_string_index] if not item.startswith('-----')]
        key_body: list[str] = [item for item in cert_arr[key_start_string_index:key_end_string_index] if not item.startswith('-----')]

        for ca_string in ca_body:
            cert_arr.pop(cert_arr.index(ca_string))

        for cert_string in key_body:
            cert_arr.pop(cert_arr.index(cert_string))

        cert_body: list[str] = [item for item in cert_arr if not item.startswith('-----')]

        if len(ca_body) == 0 or len(ca_body) == 0 or len(ca_body) == 0:
            raise ValueError('cert_parser -> Вернул пустой список')

        return CertBlocksDTO(
            cert_body=ca_body,
            ca_body=cert_body,
            key_body=key_body,
        )

    @classmethod
    def get_cretificate_routes(cls, cert_routs: CertificateDTO) -> list[str] | Exception:
        """Get attached routes"""

        return cert_routs

    @classmethod
    def get_certifacate_template(cls, template_name: str, blocks_dict: CertBlocksDTO) -> str:
        """Prepeare certificate template for Jinja"""

        env = Environment(loader=FileSystemLoader(f'{INFOSEQ_ROOT}/user_certificates/templates/'))
        template = env.get_template(template_name)
        certificate_template = template.render(blocks_dict).strip()

        return certificate_template

    @classmethod
    def ovpn_certificate_create(cls, cert_template: str, ovpn_certificate_name: str) -> str | Exception:
        """Create final certificate file with blocks and routes"""

        new_ovpn_cert_file_path: str = f'{INFOSEQ_ROOT}/user_certificates/ovpn_certificates'

        with open(f'{new_ovpn_cert_file_path}/{ovpn_certificate_name}.ovpn', 'w') as final_cert:
            final_cert.writelines(cert_template)
        
        return f'{new_ovpn_cert_file_path}/{ovpn_certificate_name}.ovpn'

    @classmethod
    def cert_template_cleaner(cls, cetrificate_storage_path: str) -> None:
        """Remove *.p12 and *.crt files from storage"""

        tmp_certificate_extension = '{*.p12,*.crt}'
        cleaner = subprocess.run(f'rm {cetrificate_storage_path} {tmp_certificate_extension}',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True, check=True
            )

        if cleaner.returncode != '0':
            raise ValueError('cert_template_cleaner -> Венул ошибку')

    @classmethod
    def certificate_reissue(cls, certificate_dto: CertificateDTO) -> dict[str: any]:
        """"""
        pass

    @classmethod
    def certificate_lifetime_check(cls) -> None:
        """Search active cetificates and send email to emplyee"""

        actual_certificates: QuerySet = InfoSeqUserCertficateModel.objects.select_related('employee').filter(is_active=True)
        for i in actual_certificates:
            cert_end_date = (i.create_at.date() + datetime.timedelta(days=365)) - datetime.datetime.now().date()
            if cert_end_date.days > 5:
                print(i.employee.email)
