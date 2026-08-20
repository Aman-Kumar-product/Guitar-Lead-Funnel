try:
    from backend.main import app
except Exception as e:
    import traceback
    error_traceback = traceback.format_exc()
    
    from http.server import BaseHTTPRequestHandler
    class handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(f"Import Failed:\n\n{error_traceback}".encode('utf-8'))
            return
    app = handler
