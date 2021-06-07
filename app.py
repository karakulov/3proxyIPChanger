from flask import Flask, request, abort
import json

app = Flask(__name__)

AUTH_CODE = '12345'
FILENAME_CLIENTS = 'clients.json'
FILENAME_IPS = 'iplist.txt'
FILENAME_UPDATE = 'update'
LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 7777

clients = {}


@app.route('/ping/<client_id>', methods=['GET'])
def ping(client_id):
    if 'AUTH' not in request.headers or request.headers['AUTH'] != AUTH_CODE:
        abort(403)

    if client_id in clients.keys() and request.remote_addr == clients[client_id]:
        print('Изменений не обнаружено {} -> {}'.format(client_id, request.remote_addr))
        return 'NO CHANGES'

    clients[client_id] = request.remote_addr

    # Обновление таблицы клиентов
    with open(FILENAME_CLIENTS, 'w') as f:
        json.dump(clients, f)

    ips = list(clients.values())
    ip_string = ",".join(ips)

    # Обновление файла со списком разрешенных IP
    with open(FILENAME_IPS, 'w') as f:
        f.write(ip_string)

    print("Обновлен список разрешенных IP: {}".format(ips))

    # Обновление файла-флага для перезапуска 3proxy
    with open(FILENAME_UPDATE, 'w') as f:
        f.write('1')

    return 'OK'


if __name__ == '__main__':
    with open(FILENAME_CLIENTS, 'r') as f:
        clients = json.load(f)

    # app.debug = True
    # app.run()

    from waitress import serve
    serve(app, host=LISTEN_IP, port=LISTEN_PORT)
