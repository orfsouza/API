import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

API_URL = "https://casino.betfair.com/api/tables-details"

def obter_resultado():
    response = requests.get(API_URL)
    if response.status_code != 200:
        return []
    data = response.json()
    data = data['gameTables']
    for x in data:
        if x['gameTableId'] == '48z5pjps3ntvqc1b':  # ID da roleta
            try:
                return x['lastNumbers']
            except KeyError:
                continue
    return []

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/roleta':
            resultado = obter_resultado()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servindo na porta {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
