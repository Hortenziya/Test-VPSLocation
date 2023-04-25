from typing import Dict

import requests


class Server:
    def __init__(self, closest_vps, file_link):
        self.closest_vps = closest_vps
        self.file_link = file_link

    def get_details_of_closest_vps(self):
        response = self.send_link(self.closest_vps)
        return self.create_dict(self.closest_vps, response)

    def get_details_of_rest_vps(self, servers):
        download_to_server = []
        response_per_server = {}
        for server in servers:
            if server != self.closest_vps:
                response = self.send_link(server)
                download_to_server.append(server['name'])

                response_per_server[server['name']] = self.create_dict(
                    server, response
                )

        return [download_to_server, response_per_server]

    # def get_access_to_info(self, download_to_server, downloaded_server):
    #     for name in download_to_server:
    #         server_details = downloaded_server[name]
    #         downloading_details_response: Dict = server_details['response']

    def send_link(self, vps_url):
        response = requests.post(
            vps_url['url'] + '/upload',
            json={'link': self.file_link, 'url': vps_url['url']}
        )
        return response.json()

    def create_dict(self, vps, response):
        return {
            'name': vps['name'],
            'city': vps['city'],
            'ip': vps['ip'],
            'response': response
        }
