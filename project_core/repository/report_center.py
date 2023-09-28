# Utils
from datetime import datetime
from pathlib import Path
import subprocess
import json

# ProjectSettings
from web_core.settings import INFOSEQ_ROOT

# DTO
from utils.dto import (
    ReportListDTO,
    CDPParsedDataDTO,
    LanParsedReportDTO,
    ParsedReportsDTO,
    )


class ReportControlCenter:
    """Base infoseq report managment"""

    """
    TODO:
    1. Проработать алгоритм извлечения и объединения данных для LAN отчетов:
        * Упаковать распарсенные данные из LAN отчета в DTO
    2. Проработать конвертацию lldp.pcap в lldp.json.
    3. Проработать извлечение данных из lldp.json отчета:
        * Упаковать распарсенные данные из LLDP отчета в DTO
    4. Проработать формат возвращаемых данных:
        * Список списков
        * Словарь
        * DTO(CDP_DTO, LLDP_DTO, LAN_DTO)
    5. Проработать удаление остаточных файлов.
    6. Проработать парсер отчетов нагрузка на канал.
    """

    @classmethod
    def _manager(cls):
        """Report full cycle manager"""

        report_path_postfix: str = 'infoseq_reports'
        base_report_storage_path: str = f'{INFOSEQ_ROOT}/{report_path_postfix}'
        formated_current_date: datetime = datetime.now().date().strftime('%b-%d-%Y').lower()

        try:
            # Подготавливет хранилище
            current_report_dir_path: str = cls.reports_storage_preparation(
                formated_current_date=formated_current_date,
                base_report_storage_path=base_report_storage_path,
            )

            # Собирает файлы отчетов по расширению
            report_files_list: list[ReportListDTO] = cls.report_flile_aggregator(
                base_report_storage_path=base_report_storage_path,
            )

            # Форматирует и перезаписывает файлы отчетов
            parsed_reports_dto_list: list[ParsedReportsDTO] = cls.file_reports_parser(
                report_files_list=report_files_list,
                current_report_dir_path=current_report_dir_path,
                formated_current_date=formated_current_date,
            )

            return parsed_reports_dto_list

        except Exception as error:
            print(f'ReportControlCenter -> Вернул {error}')

    @classmethod
    def reports_storage_preparation(cls, formated_current_date: str, base_report_storage_path: str) -> str:
        """Check or create report storage"""

        report_dir_path: str = Path(f'{base_report_storage_path}/{formated_current_date}')

        if Path.exists(report_dir_path):
            return report_dir_path

        else:
            Path.mkdir(report_dir_path)
            return report_dir_path

    @classmethod
    def report_flile_aggregator(cls, base_report_storage_path: str) -> list[str] | Exception:
        """Aggregate report files"""

        lan_report_files_list: list[Path] = []
        cdp_report_files_list: list[Path] = []
        lldp_report_files_list: list[Path] = []

        report_files_list: list[Path] = [file for file in Path(base_report_storage_path).iterdir() if file.is_file()]

        for item in report_files_list:
            if item.name.split('.')[-1] == 'txt' and not item in lan_report_files_list:
                lan_report_files_list.append(item)

            elif item.name.split('.')[0].split('_')[1] == 'cdp' and not item in cdp_report_files_list:
                cdp_report_files_list.append(item)

            elif item.name.split('.')[0].split('_')[0] == 'lldp' and not item in lldp_report_files_list:
                lldp_report_files_list.append(item)

        if len(lan_report_files_list) > 0 or len(cdp_report_files_list) > 0 or len(lldp_report_files_list) > 0:
            return ReportListDTO(
                lan_report_list=lan_report_files_list,
                cdp_report_list=cdp_report_files_list,
                lldp_report_list=lldp_report_files_list
            )

        raise ValueError('report_flile_aggregator -> Вернул пустой список')

    @classmethod
    def file_reports_parser(cls, report_files_list: list[ReportListDTO], current_report_dir_path: str, formated_current_date: str) -> list:
        """Parse and format *.pcap & *.txt report"""

        cdp_mac_list: list[str] = []
        dto_list: list[list[str]] = []

        HEADERS: dict = LanParsedReportDTO.__annotations__.keys()

        # LAN REPORT FORMATTER (Собираем все в один файл)
        for lan_key in report_files_list.lan_report_list:
            with open(lan_key, 'r') as lan_template:
                lan_arr: list[str] = [
                    item.strip().split('\t') for item in lan_template.readlines() if item.startswith('192')
                ]

                for i in lan_arr[1:]:
                    if len(i) < 5:
                        i += '0' * 5
                        # print(i)


                # parsed_data[1].net_bios_name -> net_bios_name
                parsed_data: list[LanParsedReportDTO] = [
                    LanParsedReportDTO(
                    **dict(zip(HEADERS, row))) for row in lan_arr if len(row) > 4
                ]

        # CDP REPORT PARSER
        for cdp_key in report_files_list.cdp_report_list:
            convert_cdp_pcap = subprocess.run(f'tshark -r {cdp_key} -T json', stdout=subprocess.PIPE, shell=True, check=True)
            arr_cdp_pcap: list[list[str]] = [item for item in json.loads(convert_cdp_pcap.stdout.decode('utf8').replace("'", '"'))]

            # GET CDP DTO (Platform, ip, mac)
            for cdp_report_string in arr_cdp_pcap:

                # Отсеиваем МАС адреса
                if cdp_report_string.get('_source').get('layers').get('eth').get('eth.src') not in cdp_mac_list:
                    cdp_mac_list.append(cdp_report_string.get('_source').get('layers').get('eth').get('eth.src'))

                    # Собираем IP-Адреса
                    for item in cdp_report_string.get('_source').get('layers').get('cdp').get('Addresses').values():
                        if type(item) == dict:
                            dto_list.append(
                                CDPParsedDataDTO(
                                    platform = cdp_report_string.get('_source').get('layers').get('eth').get('eth.src_tree').get('eth.src_resolved'),
                                    ip = item.get('cdp.nrgyz.ip_address'),
                                    mac = cdp_report_string.get('_source').get('layers').get('eth').get('eth.src'),
                                )
                            )

        # LLDP REPORT PARSER
        for lldp_key in report_files_list.lldp_report_list:
            convert_lldp_pcap = subprocess.run(f'tshark -r {lldp_key} -T json', stdout=subprocess.PIPE, shell=True, check=True)
            arr_lldp_pcap: list[list[str]] = [item for item in json.loads(convert_lldp_pcap.stdout.decode('utf8').replace("'", '"'))]

        for i in dto_list:
            print(i)

        if len(dto_list) > 0:
            return dto_list

        raise ValueError('file_reports_formatter -> Вернул пустой список dto_list')


class TraficMonitor:
    """"""

    @classmethod
    def _manager(cls):
        """"""

        with open(f'{INFOSEQ_ROOT}/infoseq_reports/test.txt') as trafic_report:
            trafic_arr = [item.strip() for item in trafic_report.readlines() if not item.startswith('------------------------------')\
                        and not item.startswith('============================')\
                        and not item.startswith('Total')\
                        and not item.startswith('Peak')\
                        and not item.startswith('Cumulative')\
                        and not item.endswith('cumulative')\
                        ]
            for i in trafic_arr:
                if '<=' in i:
                    print(i)
