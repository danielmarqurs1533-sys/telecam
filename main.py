from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from call_manager import CallManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://id-preview--8d57d98e-0028-4cbb-9f28-2231ed03838a.lovable.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = CallManager()

class StartCallRequest(BaseModel):
    api_id: str
    api_hash: str
    phone_number: str
    target_contact: str
    media_url: str

class StopCallRequest(BaseModel):
    call_id: str

@app.post("/api/start-call")
async def start_call(req: StartCallRequest):
    try:
        result = await manager.start_call(
            api_id=int(req.api_id),
            api_hash=req.api_hash,
            phone=req.phone_number,
            target=req.target_contact,
            media_url=req.media_url
        )
        return {"success": True, "call_id": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stop-call")
async def stop_call(req: StopCallRequest):
    try:
        await manager.stop_call(req.call_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{call_id}")
async def call_status(call_id: str):
    return manager.get_status(call_id)

@app.get("/health")
async def health():
    return {"status": "ok"}
