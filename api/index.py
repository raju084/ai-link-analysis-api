import sys
import os
from urllib.parse import parse_qs, urlencode

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Functions.
    Resolves the original request path from the 'path' query parameter set by Vercel rewrite.
    """
    if scope.get("type") == "http":
        qs_bytes = scope.get("query_string", b"")
        if qs_bytes:
            params = parse_qs(qs_bytes.decode("latin1", errors="replace"), keep_blank_values=True)
            if "path" in params:
                raw_path = params.pop("path", [""])[0]
                scope["path"] = "/" + raw_path.lstrip("/")
                scope["query_string"] = urlencode(params, doseq=True).encode("latin1")
            elif scope.get("path") in ("/api/index.py", "/api/index", "/api"):
                scope["path"] = "/"
        else:
            if scope.get("path") in ("/api/index.py", "/api/index", "/api"):
                scope["path"] = "/"

    await fastapi_app(scope, receive, send)
