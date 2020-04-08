import os
import socket
import command_line
from multiprocessing.dummy import Pool as ThreadPool
from myhttp.request import HttpRequest, parse_http_request
from myhttp.methods import HttpMethod
from myhttp.response import HttpResponse, HttpSendResponseBody
from myhttp.content_type import HttpContentType, uri_to_content_type
from myhttp.connection_type import HttpConnectionType
from myhttp import HTTP_OK, HTTP_NOT_FOUND, PACKET_SIZE, HTTP_FORBIDDEN

def send_response(client, response: HttpResponse, method: HttpMethod):
    if method == HttpMethod.GET:
        client.sendall(str(response).encode() + response.body.get_content())
    if method == HttpMethod.HEAD:
        client.sendall(str(response).encode())

def handle_connection(server_socket):
    while True:
        client, address = server_socket.accept()
        client.settimeout(15)
        connection_type: HttpConnectionType = HttpConnectionType.KEEP_ALIVE
        while connection_type == HttpConnectionType.KEEP_ALIVE:
            try:
                client_request_raw = client.recv(PACKET_SIZE)
            except:
                client.close()
                break
            client_request = client_request_raw.decode()
            if len(client_request) <= 0: 
                continue

            request: HttpRequest = parse_http_request(client_request)
            connection_type = request.connection_type

            print (request)
            print ('')  # new line

            uri: str = request.uri

            # only handle 1 request (get the auth logs)

            if uri == '/log':
                os.system('cat /var/log/auth.log > log.txt')
                response: HttpResponse = HttpResponse(HTTP_OK, HttpSendResponseBody('log.txt', uri_to_content_type('log.txt'), connection_type))
                send_response(client, response, request.method)
                continue

            # not valid request
            send_response(client, HTTP_NOT_FOUND, request.method)
        
#
#            if uri == '/' or uri == '':
#                send_response(client, HttpResponse(HTTP_OK, HttpSendResponseBody('Upload/index.html', HttpContentType.TEXT_HTML, connection_type)), request.method)
#                continue
#            
#            if not uri.startswith('/Upload/'):
#                uri = 'Upload/' + uri
#
#            absolute_uri: str = os.path.abspath(uri)
#
#            permission = os.stat(absolute_uri).st_mode & 0o004
#
#            if (not 'Upload' in absolute_uri and os.path.exists(absolute_uri)) or permission != 0o004:
#                send_response(client, HTTP_FORBIDDEN, request.method)
#                continue
#
#            if not os.path.exists(absolute_uri):
#                send_response(client, HTTP_NOT_FOUND, request.method)
#                continue
#
#            response: HttpResponse = HttpResponse(HTTP_OK, HttpSendResponseBody(uri, uri_to_content_type(request.uri), connection_type))
#            send_response(client, response, request.method)

        client.close()

def run_server(port: int) -> None:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))

    server_socket.listen(5)

    thread_pool = ThreadPool(5)

    thread_pool.map(handle_connection, [server_socket])

    #handle_connection(server_socket)
    
    thread_pool.close()
    thread_pool.join()

def main():
    port: int = command_line.get_port(1)
    run_server(port)    

if __name__ == '__main__':
    main()
        
