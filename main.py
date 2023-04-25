from flask import Flask, render_template, request, send_from_directory

from location import Location, Host
from replication import Replication
from upload import FileUpload

app = Flask(__name__)

servers = [
    {
        'name': 'VPS1',
        'city': 'Frankfurt',
        'location': (50.110258, 8.682471),
        'ip': '104.238.177.11',
        'url': 'http://104.238.177.11:5001'
    },
    {
        'name': 'VPS2',
        'city': 'Chicago',
        'location': (41.877054, -87.629422),
        'ip': '45.76.26.184',
        'url': 'http://45.76.26.184:5001'
    },
    {
        'name': 'VPS3',
        'city': 'Bangalore',
        'location': (12.974303, 77.592612),
        'ip': '139.84.143.243',
        'url': 'http://139.84.143.243:5001'
    },
]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
async def send_link_to_vps():
    file_link = request.form['url']
    location_file = Host(link=file_link).get_object_location()

    # Завантажуємо на VPS, найближчу до файлу
    closest_vps = Location(servers, location_file).get_closest_server()
    initial_upload_result = await Replication(
        closest_vps,
        file_link
    ).upload_to_closest_vps()

    # Завантажуємо на інші VPS, використовуючи нове посилання
    initial_upload_link = initial_upload_result['response']['download_url']
    replication_order, replication_responses = await Replication(
        closest_vps, initial_upload_link
    ).upload_to_other_servers(servers)

    server_details_2 = replication_responses[replication_order[0]]
    server_details_3 = replication_responses[replication_order[1]]

    return render_template(
        'success.html',
        vps_name_1=closest_vps['name'],
        vps_city_1=closest_vps['city'],
        vps_ip_1=closest_vps['ip'],
        upload_duration_1=initial_upload_result['response']['upload_duration'],
        upload_time_1=initial_upload_result['response']['upload_time'],
        url_for_download_1=initial_upload_result['response']['download_url'],

        vps_name_2=server_details_2['name'],
        vps_city_2=server_details_2['city'],
        vps_ip_2=server_details_2['ip'],
        upload_duration_2=server_details_2['response']['upload_duration'],
        upload_time_2=server_details_2['response']['upload_time'],
        url_for_download_2=server_details_2['response']['download_url'],

        vps_name_3=server_details_3['name'],
        vps_city_3=server_details_3['city'],
        vps_ip_3=server_details_3['ip'],
        upload_duration_3=server_details_3['response']['upload_duration'],
        upload_time_3=server_details_3['response']['upload_time'],
        url_for_download_3=server_details_3['response']['download_url'],

        file_name=file_link.split('/')[-1]
    )


@app.route('/upload', methods=['POST'])
def get_link_to_file():
    file_link = request.json['link']
    server_url = request.json['url']
    upload_to_vps = FileUpload('uploads/').upload_to_vps(file_link, server_url)
    return upload_to_vps


@app.route('/download_info/<filename>', methods=['GET'])
def get_closest_vps_download_info(filename):
    user_ip_address = request.remote_addr
    location_user = Host(ip_address=user_ip_address).get_object_location()
    closest_vps_to_user = Location(servers, location_user).get_closest_server()

    vps_host = Host(link=closest_vps_to_user['url'])
    location_vps = vps_host.get_object_location()

    download_url = closest_vps_to_user['url'] + '/' + filename
    return {
        'vps_name': closest_vps_to_user['name'],
        'vps_ip': vps_host.ip_address,
        'vps_city': location_vps['city'],
        'download_url': download_url
    }


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(
        'uploads/', filename, download_name=filename
    )


if __name__ == '__main__':
    app.run(port=5001)
