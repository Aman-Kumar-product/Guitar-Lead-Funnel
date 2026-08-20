try:
    from backend.main import app
except Exception as e:
    import traceback
    from fastapi import FastAPI
    app = FastAPI()
    
    error_traceback = traceback.format_exc()
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all(path: str):
        return {"error": "Import Failed", "traceback": error_traceback}
