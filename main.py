import sys
import os
import traceback

root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app.main import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    app = FastAPI()
    err_tb = traceback.format_exc()
    @app.api_route("/{path_name:path}", methods=["GET", "POST"])
    async def error_handler(path_name: str):
        return JSONResponse({"import_error": str(e), "traceback": err_tb}, status_code=500)
