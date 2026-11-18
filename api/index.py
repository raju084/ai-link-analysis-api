import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Functions.
    Restores original requested path from Vercel edge proxy headers.
    """
    if scope.get("type") == "http":
        headers = dict(scope.get("headers", []))
        
        orig = (
            headers.get(b"x-forwarded-uri") or 
            headers.get(b"x-matched-path") or 
            headers.get(b"x-real-path") or
            headers.get(b"x-now-route-matches")
        )
        
        if orig:
            orig_str = orig.decode("utf-8", errors="replace").split("?")[0]
            if "docs" in orig_str:
                scope["path"] = "/docs"
            elif "openapi" in orig_str:
                scope["path"] = "/openapi.json"
            elif "health" in orig_str:
                scope["path"] = "/health"
            elif "link-analysis" in orig_str:
                scope["path"] = "/link-analysis"
            elif orig_str and not orig_str.startswith("/api/index"):
                scope["path"] = orig_str
            else:
                scope["path"] = "/"
        else:
            current = scope.get("path", "/")
            if current in ("/api/index.py", "/api/index", "/api"):
                scope["path"] = "/"

    await fastapi_app(scope, receive, send)
