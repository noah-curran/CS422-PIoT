from enum import Enum

class HttpMethod(Enum):
    GET = 'GET'
    HEAD = 'HEAD'

    def __str__(self):
        return self.value

def parse_http_method(string: str) -> HttpMethod:
    if string == str(HttpMethod.GET):
        return HttpMethod.GET
    if string == str(HttpMethod.HEAD):
        return HttpMethod.HEAD
    
    # default
    return HttpMethod.GET

