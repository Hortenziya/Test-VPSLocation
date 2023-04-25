import requests


class Replication:
    def __init__(self, closest_vps, file_link):
        self.closest_vps = closest_vps
        self.file_link = file_link

    def upload_to_closest_vps(self):
        response = self.upload_to_vps(self.closest_vps)
        return self.create_dict(self.closest_vps, response)

    def upload_to_other_servers(self, servers):
        download_to_server = []
        response_per_server = {}
        for server in servers:
            if server != self.closest_vps:
                download_to_server.append(server['name'])
                response = self.upload_to_vps(server)
                response_per_server[server['name']] = self.create_dict(
                    server, response
                )

        return [download_to_server, response_per_server]

    def upload_to_vps(self, vps_url):
        response = requests.post(
            vps_url['url'] + '/upload',
            json={'link': self.file_link, 'url': vps_url['url']}
        )
        return response.json()

    @staticmethod
    def create_dict(vps, response):
        return {
            'name': vps['name'],
            'city': vps['city'],
            'ip': vps['ip'],
            'response': response
        }
