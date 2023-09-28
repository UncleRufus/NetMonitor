# Utils
import string
from random import sample
from django.utils.text import slugify
from transliterate import translit

# DTO
from utils.dto import KeyPassDTO


def employee_options_translitirate(employee_dto: dict[str: any]) -> dict[str: str]:
    """"""

    department: str = slugify(translit(str(employee_dto.depatment), 'ru', reversed=True))
    position: str = slugify(translit(str(employee_dto.position), 'ru', reversed=True))

    return {
        'department': department,
        'position': position,
    }


def user_sertificate_name_formatter(employee_name: str) -> str:
    """Join name prefix to certificate name"""

    cert_prefix_template: str = 'ovpn-client'
    cert_employee_tmp: str = slugify(translit(str(employee_name), 'ru', reversed=True))
    certificate_name = f'{cert_prefix_template}-{cert_employee_tmp}'
    return certificate_name


def user_password_generator() -> tuple[str]:
    """Gnerate key and password for user certificate"""

    letters: str = string.ascii_lowercase
    capital_letters: str = string.ascii_uppercase
    numbers: str = string.digits

    arr: str = letters + capital_letters + numbers
    passwd: str = ''.join(sample(arr, 20))
    key: str = ''.join(sample(arr, 20))
    return KeyPassDTO(
        key=key,
        passwd=passwd,
    )
