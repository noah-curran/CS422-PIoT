from enum import Enum

class HttpConnectionType(Enum):
    KEEP_ALIVE = 'keep-alive'
    CLOSED = 'Closed'

    def __str__(self):
        return self.value

def parse_http_connection_type(connection_type: str) -> HttpConnectionType:
    if connection_type == 'keep-alive':
        return HttpConnectionType.KEEP_ALIVE
    if connection_type == 'Closed':
        return HttpConnectionType.CLOSED