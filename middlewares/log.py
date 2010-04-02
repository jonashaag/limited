from time import time
from limited.settings import MEDIA_URL, ADMIN_URL
from limited.settings import LOGGING_OPTIONS

def truncate_server_address(address):
    """
    Replaces the first and last part of ip `address` with XXX.
    >>> truncate_server_address('127.0.0.1')
    'XXX.0.0.XXX'
    """
    return '.'.join(['XXX']+address.split('.')[1:-1]+['XXX'])

class LoggingMiddleware(object):
    fobj = None

    def __init__(self):
        self.fobj = open(LOGGING_OPTIONS.get('filename', 'access.log'), 'a')
        self.include_media = LOGGING_OPTIONS.get('inlude_media', False)
        self.include_admin = LOGGING_OPTIONS.get('inlude_admin', False)

    def process_response(self, request, response):
        if (request.path.startswith(MEDIA_URL) and not self.include_media) or \
           (request.path.startswith(ADMIN_URL) and not self.include_admin):
            # pass logging
            return response
        self.log(request, response)
        return response

    def log(self, request, response):
        self.fobj.write('%s\n' % ' || '.join(map(str, [
            time(),
            truncate_server_address(request.META['REMOTE_ADDR']),
            request.path,
            response.status_code
            ])))
        self.fobj.flush()
