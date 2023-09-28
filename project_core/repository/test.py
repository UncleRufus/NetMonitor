# Utils
import socket

# ProjectSettings
from web_core.settings import INFOSEQ_ROOT

# BUFFER = 4096

# sock = socket.socket()
# sock.bind(('', 9090))
# sock.listen(1)

# print(f'Socket NAME: {sock.getsockname()}')


def test_parser():

    http_port_ip_list: list[str] = []
    printer_ports_list: list[str] = []
    ftp_ports_list: list[str] = []
    phone_list: list[str] = []

    with open(f'{INFOSEQ_ROOT}/infoseq_reports/masscan_log.txt', 'r') as tmp_report:
        report_arr: list[str] = [item.strip() for item in tmp_report]
        print(f'LEN REPORT ARRAY: {len(report_arr)}')
        for report_string in report_arr:
            if ' 80/tcp' in report_string and report_string not in http_port_ip_list:
                http_port_ip_list.append(report_string)

            if ' 80/tcp' and '515/tcp' and ' 21/tcp' in report_string and report_string not in printer_ports_list:
                printer_ports_list.append(report_string)

            if ' 80/tcp' and ' 5060/tcp' in report_string and report_string not in phone_list and report_string not in http_port_ip_list:
                phone_list.append(report_string)

            if ' 21/tcp' in report_string and report_string not in ftp_ports_list and report_string not in printer_ports_list:
                ftp_ports_list.append(report_string)

    print('--== DEBUG ==--')
    print(f'HTTP PORTS [{len(http_port_ip_list)}]: {http_port_ip_list}')
    print('-'*50)
    print(f'PRINTERS [{len(printer_ports_list)}]: {printer_ports_list}')
    print('-'*50)
    print(f'FTP PORTS [{len(ftp_ports_list)}]: {ftp_ports_list}')
    print('-'*50)
    print(f'PHONES [{len(phone_list)}]: {phone_list}')
    print('='*50)
