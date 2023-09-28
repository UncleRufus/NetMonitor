# Utils
import json
import datetime
import http.server


global_employee_list = []


class LocalIncomingHttpServer(http.server.SimpleHTTPRequestHandler):
    """HTTP local server"""

    def _send_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self) -> None:
        """Base POST method"""

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data: str = post_data.decode('utf8').replace("'", '"')
        json_data: dict[str: str] = json.loads(data)

        log_id_list: list[int] = []

        for log_record in json_data.get('logs'):
            # Получаем дату события
            responce_date = datetime.datetime.fromtimestamp(log_record.get('time'))
            current_hour: int = responce_date.time().hour - 3

            # Записываем логи событий чтбы вытащить последный
            if log_record.get('logId') not in log_id_list:
                log_id_list.append(log_record.get('logId'))

            # Если день события == сегодня и час события >= 9
            if responce_date.date().day == datetime.datetime.now().date().day and current_hour >= 9:

                # Если направление == вход и ID карточки нет в списке, записываем ID карточек
                if log_record.get('direction') == 2 and log_record.get('keyHex') not in global_employee_list:
                    global_employee_list.append(log_record.get('keyHex'))
                    print(f"{log_record.get('keyHex')}/{responce_date.time()}")

        responce_date = {"confirmedLogId":int(log_id_list[-1])}

        send_data = json.dumps(responce_date).encode("utf-8")
        self._send_response()
        self.wfile.write(send_data)

    def do_GET(self) -> None:
        """Base GET method"""

        send_data = json.dumps(global_employee_list).encode("utf-8")
        self._send_response()
        self.wfile.write(send_data)


if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", 9090), LocalIncomingHttpServer)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print('Сервер остановлен вручную')
