import sys
import os
from urllib.parse import parse_qs, urlencode

# Ensure the root directory is on the Python path for Vercel Serverless
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Functions.
    Restores the true requested path from the Vercel rewrite parameter.
    """
    if scope.get("type") == "http":
        query_bytes = scope.get("query_string", b"")
        if query_bytes:
            qs = parse_qs(query_bytes.decode("utf-8", errors="replace"), keep_blank_values=True)
            if "match" in qs:
                match_val = qs.pop("match")[0]
                scope["path"] = "/" + match_val.lstrip("/")
                # Re-encode remaining query parameters
                scope["query_string"] = urlencode(qs, doseq=True).encode("utf-8")
        elif scope.get("path") in ("/api/index.py", "/api/index", "/api"):
            scope["path"] = "/"

    await fastapi_app(scope, receive, send)
