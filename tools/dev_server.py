"""
dev_server.py
=============
Local development server for OmniMatrix website with live folder scanning.
- Serves static HTML, CSS, JS, Images, Video
- Dynamically scans website-assets/ on every request to /api/gallery.php (same as GoDaddy PHP)
- Auto-opens your default web browser to http://localhost:8000
"""

import os, sys, json, time, glob, webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "website-assets")

GALLERY_MAP = {
    "lab-products":     "3-Products-Laboratory-Plasticware",
    "injection-molds":  "4-Services-Injection-Molds",
    "press-tools":      "5-Services-Press-Tools",
    "die-casting":      "6-Services-Die-Casting",
    "jigs-fixtures":    "7-Services-Jigs-Fixtures",
    "spm-automation":   "8-Services-SPM-Automation",
    "service1-gallery": "4-Services-Injection-Molds",
    "service2-gallery": "5-Services-Press-Tools",
    "service3-gallery": "6-Services-Die-Casting",
    "service4-gallery": "7-Services-Jigs-Fixtures",
    "service5-gallery": "6-Services-Die-Casting",
    "service6-gallery": "8-Services-SPM-Automation",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        # Handle live gallery scan request
        if self.path.startswith('/api/gallery.php') or self.path.startswith('/api/gallery'):
            manifest = {}
            v = int(time.time())
            for key, folder_name in GALLERY_MAP.items():
                folder_path = os.path.join(ASSETS_DIR, folder_name)
                images = []
                if os.path.isdir(folder_path):
                    for fname in sorted(os.listdir(folder_path)):
                        ext = os.path.splitext(fname)[1].lower()
                        if ext in IMAGE_EXTS:
                            images.append(f"../website-assets/{folder_name}/{fname}?v={v}")
                manifest[key] = images

            data = json.dumps(manifest, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        # Default static file serving
        return super().do_GET()

def run(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    url = f"http://localhost:{port}"
    print("=" * 60)
    print(f"  OmniMatrix Local Server Running at: {url}")
    print("  Live Folder Scanning Active (same as GoDaddy PHP)")
    print("  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Auto-open browser
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run(port)
