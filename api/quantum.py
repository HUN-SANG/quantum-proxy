from http.server import BaseHTTPRequestHandler
import json, os
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length > 0 else b'{}'
            data = json.loads(body.decode('utf-8'))
            
            token = os.environ.get('IBM_QUANTUM_TOKEN')
            if not token:
                self.send_json(400, {'error': 'TOKEN required'})
                return
            
            from qiskit_ibm_runtime import QiskitRuntimeService
            service = QiskitRuntimeService(channel="ibm_cloud", token=token)
            
            if data.get('action') == 'test':
                backends = service.backends()
                result = {'success': True, 'backends': len(backends)}
            else:
                result = {'success': True, 'symbol': data.get('symbol', 'ARWR')}
            
            self.send_json(200, result)
        except Exception as e:
            self.send_json(500, {'error': str(e)})
    
    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
