# -*- coding: utf-8 -*-
import http.server
import sys
import time


class Handler(http.server.SimpleHTTPRequestHandler):
    """This class overrides method toHttp show request headers
    """

    def do_GET(self):
        time.sleep(5)
        super().do_GET()
        print(self.headers)


def main():
    port = int(sys.argv[1])
    server_address = ('', port)
    handler = Handler
    httpd = http.server.HTTPServer(server_address, handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
