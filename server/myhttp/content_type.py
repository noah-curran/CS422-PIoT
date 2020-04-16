from enum import Enum

class HttpContentType(Enum):
    TEXT_HTML = 'text/html'
    TEXT_PLAIN = 'text/plain'
    IMAGE_PNG = 'image/png'
    IMAGE_JPEG = 'image/jpeg'

    def __str__(self):
        return self.value

def is_text_content(content_type: HttpContentType):
    return content_type == HttpContentType.TEXT_HTML or content_type == HttpContentType.TEXT_PLAIN

def is_image_content(content_type: HttpContentType):
    return content_type == HttpContentType.IMAGE_PNG or content_type == HttpContentType.IMAGE_JPEG

def uri_to_content_type(uri: str):
    if uri.endswith('.png'):
        return HttpContentType.IMAGE_PNG
    if uri.endswith('.jpeg'):
        return HttpContentType.IMAGE_JPEG
    if uri.endswith('.txt'):
        return HttpContentType.TEXT_PLAIN
    if uri.endswith('.html'):
        return HttpContentType.TEXT_HTML

def parse_http_content_type(content_type: str) -> HttpContentType:
    if content_type == str(HttpContentType.TEXT_PLAIN):
        return HttpContentType.TEXT_PLAIN
    if content_type == str(HttpContentType.TEXT_HTML):
        return HttpContentType.TEXT_HTML
    if content_type == str(HttpContentType.IMAGE_PNG):
        return HttpContentType.IMAGE_PNG
    if content_type == str(HttpContentType.IMAGE_JPEG):
        return HttpContentType.IMAGE_JPEG

    # default
    return HttpContentType.TEXT_PLAIN