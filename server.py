
class Server:
    closest_VPS: list
    locations: dict
    current_server: dict


    def __init__(self, host):
        self.host = host

    def isNearestServer(self):
        if self.closest_VPS == self.current_server:
            return True

