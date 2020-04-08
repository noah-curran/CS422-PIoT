from . import HTTP_VERSION
from .methods import HttpMethod, parse_http_method
from .connection_type import HttpConnectionType, parse_http_connection_type
from typing import List
import re

class HttpRequest:

    def __init__(self, method: HttpMethod, uri: str, connection_type: HttpConnectionType):
        self.method = method
        self.uri = uri
        self.connection_type = connection_type

    def __str__(self):
        return str(self.method) + ' ' + self.uri + ' ' + HTTP_VERSION + f'\nConnection: {str(self.connection_type)}'

def parse_http_request(request: str) -> HttpRequest:
    parts: List[str] = request.split()
    method = parse_http_method(parts[0])
    uri = parts[1]
    capture_group = re.findall(r'Connection: (\w+\-\w+|\w+)', request)
    connection_type = capture_group[0].split()
    return HttpRequest(method, uri, parse_http_connection_type(connection_type[0]))