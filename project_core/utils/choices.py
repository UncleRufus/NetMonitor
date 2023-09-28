# Utils
from django.db import models

class VPNCertificateDestination(models.TextChoices):
    """Class for VPN certificate options"""

    WINDOWS = 'WINDOWS'
    IOS = 'IOS'
    ANDROID = 'ANDROID'
    IPAD = 'IPAD'
    IPHON = 'IPHON'
    LINUX = 'LINUX'


class VPNCertificateCountry(models.TextChoices):
    """Class for VPN certificate options"""

    RU = 'RU'


class VPNCertificateState(models.IntegerChoices):
    """Class for VPN certificate options"""

    krd = 31


class VPNCertificateOrganization(models.TextChoices):
    """Class for VPN certificate options"""

    DOGMA = 'DOGMA'
    ZAPOLYARE = 'ZAPOLYARE'


class VPNCertificateUnit(models.TextChoices):
    """Class for VPN certificate options"""

    DIS = 'DIS'


class VPNCertificateKeySize(models.TextChoices):
    """Class for VPN certificate options"""

    LARGE = '2048'


class VPNCertificateKeyUsage(models.TextChoices):
    """Class for VPN certificate options"""

    TLS = 'tls-client'


class VPNCertificateLocality(models.TextChoices):
    """Class for VPN certificate options"""

    KRD = 'KRD'
    MSK = 'MSK'
    OMK = 'OMK'
