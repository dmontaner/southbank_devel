import http.server
import socketserver
import os

PORT = 8001
DIRECTORY = os.path.join(os.path.dirname(__file__), "southbank")  # folder to serve

os.chdir(DIRECTORY)

Handler = http.server.SimpleHTTPRequestHandler

# Allow reuse of the address to prevent "Address already in use" errors
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving {DIRECTORY} at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
