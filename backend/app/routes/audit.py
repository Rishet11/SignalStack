from fastapi import APIRouter, HTTPException
from typing import List, Optional
import aiosqlite
import json
from ..database import DB_PATH
from ..schemas import AuditEntry, AuditTrail
from ..config import logger

router = APIRouter()

@router.get("/{request_id}", response_model=AuditTrail)
async def get_audit_trail(request_id: str):
    """Retrieve full audit trail for a given request ID."""
    try:
        entries = []
        ticker = ""
        completed_at = ""
        
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute("SELECT ticker, agent_name, duration_ms, status, input_data, output_data, prompt_snippet, timestamp, error_msg FROM audit_log WHERE request_id = ? ORDER BY timestamp ASC", (request_id,))
            rows = await cursor.fetchall()
            
            for row in rows:
                ticker = row[0]
                completed_at = row[7] # Last timestamp
                entries.append(AuditEntry(
                    agent_name=row[1],
                    duration_ms=row[2],
                    status=row[3],
                    input_state_summary=row[4],
                    output_state_summary=row[5],
                    llm_prompt_snippet=row[6],
                    timestamp=row[7],
                    error_message=row[8]
                ))
        
        if not entries:
            raise HTTPException(status_code=404, detail="Audit trail not found.")
            
        return AuditTrail(
            request_id=request_id,
            ticker=ticker,
            entries=entries,
            completed_at=completed_at
        )

    except Exception as e:
        logger.error(f"Error fetching audit trail for {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
