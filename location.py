import socket

import requests as requests
from geopy.distance import great_circle


class Location:
    locations: dict
    object_location: dict

    def __init__(self, locations, object_location):
        self.locations = locations
        self.object_location = object_location

    def get_closest_server(self):
        min_distance = float('inf')
        closest_server = None
        for location in self.locations:
            distance = great_circle(self.object_location['location'],
                                    location['location']).km
            if distance < min_distance:
                min_distance = distance
                closest_server = location
        return closest_server


class Host:
    link: str
    ip_address: str

    city: str
    latitude: float
    longitude: float

    def __init__(self, ip_address=None, link=None):
        self.ip_address = ip_address
        self.link = link

        if link:
            self.ip_address = self.get_ip(link)
        else:
            self.ip_address = self.ip_address

    def get_ip(self, link):
        self.link = self.link.split('/')[2]
        hostname_port = link.split('/')[2]
        hostname = hostname_port.split(':')[0]
        file_ip_address = socket.gethostbyname(hostname)
        return file_ip_address

    def get_object_location(self):
        return {'city': "Unknown", 'location': (0, 0)}

        response = requests.get(
            'https://api.ipbase.com/v2/info?'
            f'ip={self.ip_address}'
            f'&apiKey={"In4qhCO3c1qh7eOUMk53cQuB9EStKkCyWyiiHGvZ"}'
        )
        response.raise_for_status()
        location = response.json()
        city = location['data']['city']['name']
        latitude = location['data']['latitude']
        longitude = location['data']['longitude']
        return {'city': city, 'location': (latitude, longitude)}
