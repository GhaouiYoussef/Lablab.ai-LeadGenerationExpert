from fastapi import APIRouter, HTTPException
from database import discussions_collection

router = APIRouter()

@router.get("/get-discussions")
async def get_discussions():
    """Fetches discussion history from MongoDB."""
    try:
        discussions = list(discussions_collection.find({}, {"_id": 0}))
        return {"discussions": discussions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
