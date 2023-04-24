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
        hostname = link.split('/')[2]
        file_ip_address = socket.gethostbyname(hostname)
        return file_ip_address

    def get_object_location(self):
        response = requests.get(f'https://freegeoip.app/json/{self.ip_address}')
        location = response.json()
        city = location['city']
        latitude = location['latitude']
        longitude = location['longitude']
        return {'city': city, 'location': (latitude, longitude)}
