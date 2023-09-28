# Utils
import subprocess

# ProjectSettings
from web_core.settings import INFOSEQ_ROOT, PLATFORM_USER, NET_CORE

# ProjectUtils
from utils.formatters import employee_options_translitirate

# DTO
from utils.dto import CertificateOptionsDTO, CertificateDTO


class DeviceController:
    """Base device controller"""

    """
    TODO:
    1. Проработать корретное подключение к оборудованию:
        * Создать подключение, выполнить комманды, закрыть подключение.
    2. Подготовить нормальное DTO для параметров серитификата:
        * certificate_postfix;
        * connect_protocol;
        * download_protocol;
        * consol_command_prefix;
        * connector_user;
        * accepted_key;
        * net_controller_device;
    3. Проработать отправку команд на устройство (СЕЙЧАС: КАЖДАЯ КОМАНДА ОТКРЫВАЕТ И ЗАКРЫВАЕТ СОЕДИНЕНИЕ):
        * Через декоратор (открыть соединение, отправить команды, получить ответы, закрыть соединение).
    4. Проработать удаление экспортированых сертификатов на микроте;
    5. При перевыпуске сертификата проработать отключение старых РРР соединений для ползователя;
    """

    @classmethod
    def _manager(cls, command_type: str, certificate_dto: CertificateDTO, certificate_reissue: bool = None) -> None:
        """Execute and controll device"""

        employee_options: dict[str: any] = employee_options_translitirate(employee_dto=certificate_dto.employee.get_dto())
        certificate_options_dto: CertificateOptionsDTO = CertificateOptionsDTO(
            certificate_postfix = '.p12',
            connect_protocol = 'ssh',
            download_protocol = 'scp',
            consol_command_prefix = '-i /app/.ssh/core_rsa',
            connector_user = PLATFORM_USER,
            accepted_key = "-o 'PubkeyAcceptedKeyTypes +ssh-rsa'",
            net_controller_device = NET_CORE,
        )

        match command_type:
            case 'create_vpn_certificate':
                # Create certificate command
                create_cert_command: str = f'\
                    "certificate add name={certificate_dto.title} \
                    country={certificate_dto.country} \
                    state={certificate_dto.state} \
                    locality={certificate_dto.locality} \
                    organization={certificate_dto.organization} \
                    unit={certificate_dto.unit} \
                    common-name={certificate_dto.title} \
                    key-size={certificate_dto.key_size} \
                    key-usage={certificate_dto.key_usage}"'

                connect_command: str = f"\
                    {certificate_options_dto.consol_command_prefix} \
                    {certificate_options_dto.connector_user}@{certificate_options_dto.net_controller_device} \
                    {certificate_options_dto.accepted_key}"

                # Cerificate sign command {"certificate sign {certificate_dto.title} ca=ca"}
                sign_cert_command: str = f'\
                    "certificate sign {certificate_dto.title} ca=CA"'

                # PPP Create command "ppp secret add name={certificate_dto.title} password={certificate_dto.key} service=ovpn profile=OVPN_Profile_Users"
                create_ppp_command: str = f'\
                    "ppp secret add name={certificate_dto.title} \
                    password={certificate_dto.key} \
                    service=ovpn\
                    profile=OVPN_Profile_Users"\
                    comment={employee_options.get("department")}:{employee_options.get("position")}'

                # Certificate export command "certificate export-certificate {certificate_dto.title} type=pkcs12 export-passphrase={certificate_dto.passwd} file={certificate_dto.title}"
                export_cert_command: str = f'\
                    "certificate export-certificate {certificate_dto.title} \
                    type=pkcs12 export-passphrase={certificate_dto.passwd} \
                    file={certificate_dto.title}"'

                commands_list: list[str] = [
                    f'{certificate_options_dto.connect_protocol}\
                        {connect_command}\
                        {create_cert_command}',

                    f'{certificate_options_dto.connect_protocol}\
                        {connect_command}\
                        {sign_cert_command}',

                    f'{certificate_options_dto.connect_protocol}\
                        {connect_command}\
                        {create_ppp_command}',

                    f'{certificate_options_dto.connect_protocol}\
                        {connect_command}\
                        {export_cert_command}',

                    f'{certificate_options_dto.download_protocol}\
                        {certificate_options_dto.consol_command_prefix}\
                        {certificate_options_dto.accepted_key}\
                        {certificate_options_dto.connector_user}@{certificate_options_dto.net_controller_device}:{certificate_dto.title}{certificate_options_dto.certificate_postfix}\
                        {INFOSEQ_ROOT}/user_certificates/'
                ]

                try:
                    cls.send_commnad(commands_list=commands_list)
                    return f'{INFOSEQ_ROOT}/user_certificates/{certificate_dto.title}{certificate_options_dto.certificate_postfix}'

                except Exception as error:
                    print(f'DeviceController._manager -> Вернул {error}')

            case 'get_reports':
                pass

            case _:
                raise ValueError('Controller_manager -> В command_type что-то не понятное')

    @classmethod
    def send_commnad(cls, commands_list: list[str]) -> str:
        """Create connection and send commands to device"""

        for command in commands_list:

            proces = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                check=True
            )

            if proces.returncode == '0':
                continue
