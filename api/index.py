import sys
import os

# Ensure the root directory is on the Python path for Vercel Serverless
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app as fastapi_app

async def app(scope, receive, send):
    """
    ASGI entrypoint for Vercel Serverless Functions.
    Normalizes the incoming request path when Vercel rewrites to /api/index.py.
    """
    if scope.get("type") == "http":
        headers = dict(scope.get("headers", []))
        
        # Check Vercel routing headers for original path
        orig_uri = headers.get(b"x-forwarded-uri") or headers.get(b"x-matched-path") or headers.get(b"x-invoke-path")
        if orig_uri:
            scope["path"] = orig_uri.decode("utf-8").split("?")[0]
        else:
            current_path = scope.get("path", "/")
            # If Vercel passed /api/index.py or /api/index or /api, map to root
            for prefix in ("/api/index.py", "/api/index", "/api"):
                if current_path == prefix:
                    scope["path"] = "/"
                    break
                elif current_path.startswith(prefix + "/"):
                    scope["path"] = current_path[len(prefix):]
                    break

    await fastapi_app(scope, receive, send)
