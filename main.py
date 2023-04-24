import requests
from flask import Flask, render_template, request, send_from_directory

from location import Location, Host
from upload import FileUpload

app = Flask(__name__)


servers = [
    {'name': 'VPS1', 'city': 'Kolomyia', 'ip': 'need_to_get_this_info', 'location': (48.536776, 25.035782),'url': 'http://127.0.0.1:5000'},
    {'name': 'VPS2', 'city': 'Marsberg', 'ip': 'need_to_get_this_info', 'location': (51.444005, 8.799854), 'url': 'http://127.0.0.1:5000'},
    {'name': 'VPS3', 'city': 'Krakiv', 'ip': 'need_to_get_this_info', 'location': (50.047576, 20.064889), 'url': 'http://127.0.0.1:5000'},
]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def send_link_to_vps():
    file_link = request.form['url']
    location_file = Host(link=file_link).get_object_location()
    closest_vps_to_file = Location(servers, location_file).get_closest_server()

    #відправити найближчому серверу посилання від користувача
    response = requests.post(closest_vps_to_file['url']+'/upload', json={'link': file_link, 'url': closest_vps_to_file['url']})
    file_link = response.json()['download_url']

    dict_response = {closest_vps_to_file['name']: response.json()}
    closest_vps_to_file_response = dict_response[closest_vps_to_file['name']]

    download_to_server = []
    downloaded_servers = {}
    for server in servers:
        if server != closest_vps_to_file:
            response = requests.post(server['url'] + '/upload', json={'link': file_link, 'url': server['url']})
            dict_response[server['name']] = response.json()
            download_to_server.append(server['name'])

            downloaded_servers[server['name']] = {
                'name': server['name'],
                'city': server['city'],
                'ip': server['ip']
            }
    downloaded_servers_2 = downloaded_servers[download_to_server[0]]
    downloaded_servers_3 = downloaded_servers[download_to_server[1]]
    download_to_server_2_response = dict_response[download_to_server[0]]
    download_to_server_3_response = dict_response[download_to_server[1]]

    user_ip_address = request.remote_addr
    location_user = Host(ip_address=user_ip_address).get_object_location()
    closest_vps_to_user = Location(servers, location_user).get_closest_server()
    closest_vps_to_user_response = dict_response[closest_vps_to_user['name']]
    url_for_user_download = closest_vps_to_user_response['download_url']

    return render_template(
        'success.html',
        vps_name_1=closest_vps_to_file['name'],
        vps_city_1=closest_vps_to_file['city'],
        vps_ip_1=closest_vps_to_file['ip'],
        upload_duration_1=closest_vps_to_file_response['upload_duration'],
        upload_time_1=closest_vps_to_file_response['upload_time'],
        url_for_download_1=closest_vps_to_file_response['download_url'],

        vps_name_2=downloaded_servers_2['name'],
        vps_city_2=downloaded_servers_2['city'],
        vps_ip_2=downloaded_servers_2['ip'],
        upload_duration_2=download_to_server_2_response['upload_duration'],
        upload_time_2=download_to_server_2_response['upload_time'],
        url_for_download_2=download_to_server_2_response['download_url'],

        vps_name_3=downloaded_servers_3['name'],
        vps_city_3=downloaded_servers_3['city'],
        vps_ip_3=downloaded_servers_3['ip'],
        upload_duration_3=download_to_server_3_response['upload_duration'],
        upload_time_3=download_to_server_3_response['upload_time'],
        url_for_download_3=download_to_server_3_response['download_url'],

        url_for_user_download=url_for_user_download
    )


@app.route('/upload', methods=['POST'])
def get_link_to_file():
    file_link = request.json['link']
    server_url = request.json['url']
    upload_to_vps = FileUpload('uploads/').upload_to_vps(file_link, server_url)
    return upload_to_vps


@app.route('/<filename>')
def uploaded_file(filename):

    return send_from_directory(
       'uploads/', filename, download_name=filename
    )

if __name__ == '__main__':
    app.run()
