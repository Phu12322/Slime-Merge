import json
import os
import sys
import threading
import mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import webview
if getattr(sys, "frozen", False):
    EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))
    BUNDLE_DIR = getattr(sys, "_MEIPASS", EXE_DIR)
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_DIR = EXE_DIR
STORE_PATH = os.path.join(EXE_DIR, "slime_save.json")
APP_DIR = BUNDLE_DIR
DEFAULT_STORE = {"best": 0, "maxTile": 2, "totalSec": 0, "ach": [], "bg": None, "bgFit": "cover", "bgDim": 30}
def read_store():
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            merged = dict(DEFAULT_STORE)
            merged.update(data)
            return merged
    except Exception:
        pass
    return dict(DEFAULT_STORE)
def write_store(data):
    try:
        merged = dict(DEFAULT_STORE)
        if isinstance(data, dict):
            merged.update(data)
        if len(json.dumps(merged)) > 12 * 1024 * 1024:
            merged["bg"] = None
        tmp = STORE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False)
        os.replace(tmp, STORE_PATH)
        return True
    except Exception as e:
        print("save error:", e)
        return False
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=APP_DIR, **kw)
    def log_message(self, *a):
        pass
    def _send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path == "/api/state":
            return self._send_json(read_store())
        return super().do_GET()
    def do_POST(self):
        if self.path in ("/api/state", "/api/bg"):
            try:
                n = int(self.headers.get("Content-Length", "0") or 0)
            except Exception:
                n = 0
            raw = self.rfile.read(max(0, n)) if n > 0 else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8") or "{}")
            except Exception:
                payload = {}
            cur = read_store()
            if self.path == "/api/bg" and isinstance(payload, dict) and "dataUrl" in payload:
                cur["bg"] = payload.get("dataUrl")
            elif isinstance(payload, dict):
                for k in ("best", "maxTile", "totalSec", "ach", "bg", "bgFit", "bgDim"):
                    if k in payload:
                        cur[k] = payload[k]
            ok = write_store(cur)
            return self._send_json({"ok": ok})
        self.send_response(404)
        self.end_headers()
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
def main():
    mimetypes.add_type("application/manifest+json", ".json")
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/slime-merge.html"
    webview.create_window("Slime Merge", url, width=480, height=900, resizable=True, min_size=(360, 640))
    try:
        webview.start(gui="edgechromium")
    finally:
        try:
            server.shutdown()
        except Exception:
            pass
if __name__ == "__main__":
    main()
