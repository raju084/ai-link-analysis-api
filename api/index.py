import sys
import os
import json
from fastapi.responses import JSONResponse

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

async def app(scope, receive, send):
    if scope.get("type") == "http":
        headers = {k.decode("latin1"): v.decode("latin1") for k, v in scope.get("headers", [])}
        scope_copy = {k: str(v) for k, v in scope.items() if k != "headers"}
        resp = JSONResponse({
            "scope": scope_copy,
            "headers": headers
        })
        await resp(scope, receive, send)
