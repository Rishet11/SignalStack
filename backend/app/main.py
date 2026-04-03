from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .config import logger

app = FastAPI(title="SignalStack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting SignalStack API...")
    await init_db()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "SignalStack"}

from .routes import signals, ticker, audit
app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(ticker.router, prefix="/api/ticker", tags=["ticker"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
