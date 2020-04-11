import re
from enum import Enum
from typing import List
from . import HTTP_VERSION
from .content_type import (
    HttpContentType,
    is_text_content,
    is_image_content,
    parse_http_content_type,
)
from .connection_type import HttpConnectionType, parse_http_connection_type


class HttpResponseHeader:
    def __init__(self, status_code: int, reason_phrase: str):
        self.status_code = status_code
        self.reason_phrase = reason_phrase

    def __str__(self):
        s = HTTP_VERSION + " " + str(self.status_code) + " " + self.reason_phrase + "\nAccess-Control-Allow-Origin: *"
        print(s)
        return s

class HttpResponseBody:
    def __init__(
        self,
        file_name: str,
        content_type: HttpContentType,
        connection_type: HttpConnectionType,
        content_length: int,
        content,
    ):
        self.file_name = file_name
        self.content_type = content_type
        self.connection_type = connection_type
        self.content_length = content_length
        self.content = content

    def __str__(self):
        return f"Content-Length: {self.content_length}\nContent-Type: {str(self.content_type)}\nConnection: {str(self.connection_type)}\r\n\r\n"

    def get_content(self):
        return self.content

    def append_content(self, content):
        self.content = self.content + content


class HttpSendResponseBody(HttpResponseBody):
    def __init__(self, filename: str, content_type: HttpContentType, connection_type: HttpConnectionType):
        content_length = 0
        content: bytes = b'' 

        if is_text_content(content_type):
            fp = open(filename, "r")
            content = fp.readlines()
            content = "".join(content)
            content_length = len(content)
            content = content.encode()
            fp.close()

        if is_image_content(content_type):
            fp = open(filename, "rb")
            content = fp.read()
            content_length = len(content)
            fp.close()

        super().__init__(filename, content_type, connection_type, content_length, content)


class HttpReceiveResponseBody(HttpResponseBody):
    def __init__(
        self, filename: str, content_type: HttpContentType, connection_type: HttpConnectionType, content_length: int, content
    ):
        super().__init__(filename, content_type, connection_type, content_length, content)


class HttpResponse:
    def __init__(self, header: HttpResponseHeader, body: HttpResponseBody):
        self.header = header
        self.body = body

    def __str__(self):
        return str(self.header) + "\n" + str(self.body)


def parse_http_response(response, filename: str) -> HttpResponse:
    header_information = response.split(b"\r\n\r\n")[0].decode()
    parts: List[str] = header_information.split()
    status_code = int(parts[1])

    capture_group = re.findall(r"[^0-9][a-zA-Z_ ]+\n", header_information)
    reason_phrase = capture_group[0][1:]

    capture_group = re.findall(r'Connection: [\w\-]+', header_information)
    connection_type = parse_http_connection_type(capture_group[0].split()[1])

    capture_group = re.findall(r"Content-Type: [\w\/]+\n", header_information)
    content_type = parse_http_content_type(capture_group[0].split()[1])

    capture_group = re.findall(r"Content-Length: \d+\n", header_information)
    content_length = int(capture_group[0].split()[1])

    content = response.split(b"\r\n\r\n")[1]

    header = HttpResponseHeader(status_code, reason_phrase)
    body = HttpReceiveResponseBody(filename, content_type, connection_type, content_length, content)

    return HttpResponse(header, body)

