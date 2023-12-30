
import os

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging



class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.name = os.environ['REPL_SLUG']
        f = open('/home/runner/qli.log'.format(self.name), 'rb')
        data='abc'
        try:
          data= f.readlines()[-1]
        except:
          pass
        self.wfile.write("GET request for {}{}".format(self.path,data).encode('utf-8'))
        num=os.popen("export UDOCKER_DIR=/home/runner/{}/.udocker && /home/runner/{}/udocker-1.3.12/udocker/udocker ps | wc -l".format(self.name,self.name)).read()
        print(str(num))
        if int(num)<2:  
          print("rerun")
          os.system('export UDOCKER_DIR=/home/runner/{}/.udocker && nohup /home/runner/{}/udocker-1.3.12/udocker/udocker run -e cores=1 -e versionqli=1.7.9 qli | tee ../qli.log &'.format(self.name,self.name))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    name = os.environ['REPL_SLUG']
    os.system('export UDOCKER_DIR=/home/runner/{}/.udocker && nohup /home/runner/{}/udocker-1.3.12/udocker/udocker run -e cores=1 -e versionqli=1.7.9 qli | tee ../qli.log &'.format(name,name))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

