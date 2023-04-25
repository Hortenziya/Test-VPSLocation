import socket

import requests as requests
from geoip2.errors import AddressNotFoundError
from geopy.distance import great_circle
import geoip2.database

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
        try:
            with geoip2.database.Reader('GeoLite2-City/GeoLite2-City.mmdb') as reader:
                location = reader.city(self.ip_address)
                city = location.city.name
                latitude = location.location.latitude
                longitude = location.location.longitude
                return {'city': city, 'location': (latitude, longitude)}
        except AddressNotFoundError:
            return {'city': "Unknown", 'location': (0, 0)}