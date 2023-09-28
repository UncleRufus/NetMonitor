# Utils
from dataclasses import dataclass


@dataclass
class CDPParsedDataDTO:
    """DTO for CDP parsed data"""

    platform: str
    ip: str
    mac: str


@dataclass
class LLDPParsedDataDTO:
    """DTO for LLDP parsed data"""

    system_name: str
    ip: str
    vlan: str
    port: str


@dataclass
class LanParsedReportDTO:
    """DTO for lan parsed data"""

    ip_address: str | None
    tcp_ports: str | None
    udp_ports: str | None
    not_implemented: str | None
    net_bios_name: str | None


@dataclass
class ParsedReportsDTO:
    """DTO for parsed reports"""

    cdp_parced_reports: list[CDPParsedDataDTO]
    lldp_parced_reports: list[LLDPParsedDataDTO]
    lan_parced_reports: list[LanParsedReportDTO]


@dataclass
class KeyPassDTO:
    """DTO for key and password from certificate"""

    key: str
    passwd: str


@dataclass
class CertRouteDTO:
    """DTO for route"""

    title: str
    route: str


@dataclass
class CertificateDTO:
    """DTO for certificate"""

    title: str
    country: str
    state: int
    locality: str
    organization: str
    unit: str
    common_name: str
    key_size: int
    routes: list[CertRouteDTO]
    key_usage: str
    employee: str
    cert_destination: str
    passwd: str
    key: str
    repeated: bool
    created_at: str


@dataclass
class CertificateOptionsDTO:
    """DTO for crtificate options"""

    certificate_postfix: str
    connect_protocol: str
    download_protocol: str
    consol_command_prefix: str
    connector_user: str
    accepted_key: str
    net_controller_device: str


@dataclass
class CertBlocksDTO:
    """DTO for cetrificate parsed blocks"""

    cert_body: list[str]
    ca_body: list[str]
    key_body: list[str]


@dataclass
class ReportListDTO:
    """DTO for formatted reports"""

    lan_report_list: list[str]
    cdp_report_list: list[str]
    lldp_report_list: list[str]


@dataclass
class DogmaEmployeeDTO:
    """DTO for employee models"""

    first_name: str
    last_name: str
    patronymic: str
    email: str
    current_certificate: CertificateDTO
    depatment: str
    position: str


@dataclass
class DiscordOptionsDTO:
    """DTO for discord embed options"""

    event_title: str
    event_author: str
    event_footer: str


@dataclass
class SigurAccessPointDataDTO:
    """DTO for sigur incoming data"""

    access_time: str
    employee_key_hex: str
    dogma_object: str


@dataclass
class DiscordNotificationDTO:
    """DTO for discord embed notification"""

    event_type: str
    event_author: str
    event_field: str
    event_value: str
    event_content: str
    event_footer: str
