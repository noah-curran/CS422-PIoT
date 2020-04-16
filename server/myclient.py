import socket
import command_line
from typing import List, Tuple
from myhttp.request import HttpRequest
from myhttp.methods import parse_http_method
from myhttp.connection_type import HttpConnectionType
from myhttp.response import parse_http_response
from myhttp.content_type import is_image_content, is_text_content
from myhttp import PACKET_SIZE

def main():
    ip_address: str = command_line.get_ip_address(1)
    port: int = command_line.get_port(2)

    arg_count: int = 3
    requests = []
    while command_line.has_arg(arg_count) and command_line.has_arg(arg_count + 1):
        requests.append(command_line.get_request_info(arg_count))
        arg_count = arg_count + 2

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, port))

    for i in range(len(requests)):
        filename, method = requests[i]

        request = HttpRequest(
            parse_http_method(method),
            "/" + filename,
            HttpConnectionType.CLOSED
            if i == len(requests) - 1
            else HttpConnectionType.KEEP_ALIVE,
        )

        client_socket.sendall(str(request).encode())
        response = client_socket.recv(PACKET_SIZE)
        
        response_object = parse_http_response(response, filename)
    
        full_size: int = response.index(b'\r\n\r\n') + 4 + response_object.body.content_length

        bytes_read: int = PACKET_SIZE
        while bytes_read <= full_size:
            content = client_socket.recv(PACKET_SIZE)
            response_object.body.append_content(content)
            bytes_read =  bytes_read + PACKET_SIZE

        # always show header information
        print (response_object)

        if response_object.header.status_code == 403:
            filename = 'forbidden.html'
        if response_object.header.status_code == 404:
            filename = 'notfound.html'

        if is_text_content(response_object.body.content_type):
            fp = open('Download/' + filename, 'w+')
            fp.write(response_object.body.get_content().decode())
            fp.close()
        if is_image_content(response_object.body.content_type):
            fp = open('Download/' + filename, 'wb+')
            fp.write(response_object.body.get_content())
            fp.close()
            

    client_socket.close()


if __name__ == "__main__":
    main()
