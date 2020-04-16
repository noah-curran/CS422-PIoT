HTTP_VERSION = 'HTTP/1.1'
PACKET_SIZE: int = 4096

from .response import HttpResponseHeader, HttpSendResponseBody, HttpResponse
from .content_type import HttpContentType
from .connection_type import HttpConnectionType

HTTP_OK: HttpResponseHeader = HttpResponseHeader(200, 'OK')
HTTP_NOT_FOUND: HttpResponse = HttpResponse(HttpResponseHeader(404, 'NOT FOUND'), HttpSendResponseBody('assets/notfound.html', HttpContentType.TEXT_HTML, HttpConnectionType.CLOSED))
HTTP_FORBIDDEN: HttpResponse = HttpResponse(HttpResponseHeader(403, 'FORBIDDEN'), HttpSendResponseBody('assets/forbidden.html', HttpContentType.TEXT_HTML, HttpConnectionType.CLOSED))
