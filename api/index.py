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
    Resolves client request path from Vercel headers.
    """
    if scope.get("type") == "http":
        headers = dict(scope.get("headers", []))
        
        # Check if Vercel provided the original client request path
        client_uri = headers.get(b"x-forwarded-uri") or headers.get(b"x-real-path") or headers.get(b"x-now-route-matches")
        
        # If x-now-route-matches (e.g. 1=link-analysis), or x-forwarded-uri
        if headers.get(b"x-forwarded-uri"):
            scope["path"] = headers[b"x-forwarded-uri"].decode("utf-8").split("?")[0]
        else:
            raw_path = scope.get("path", "/")
            # If path was rewritten to /api/index.py, check if x-matched-path has subpath
            matched = headers.get(b"x-matched-path", b"").decode("utf-8")
            if matched and matched != "/api/index.py" and matched != "/api/index":
                scope["path"] = matched.split("?")[0]
            elif raw_path in ("/api/index.py", "/api/index", "/api"):
                # If root request
                pass

    await fastapi_app(scope, receive, send)
