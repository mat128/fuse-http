import SimpleHTTPServer
import SocketServer
import os
from BaseHTTPServer import BaseHTTPRequestHandler

PORT = 8000


class TCPServerAllowingReuse(SocketServer.TCPServer):
    allow_reuse_address = True


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_header(self, keyword, value):
        fullpath = self.translate_path(self.path)

        if 'no_content_length_for_directories' in self.path \
                and os.path.isdir(fullpath) \
                and keyword.lower() == 'content-length':
            print 'skipping content-length for {}'.format(self.path)
        else:
            BaseHTTPRequestHandler.send_header(self, keyword, value)

httpd = TCPServerAllowingReuse(("", PORT), MyHandler)

print "serving at port", PORT
httpd.serve_forever()
