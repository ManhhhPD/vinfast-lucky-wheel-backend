from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Prize
from app.schemas import PrizeResponse

router = APIRouter(prefix="/api/prizes", tags=["prizes"])


@router.get("", response_model=list[PrizeResponse])
def list_prizes(db: Session = Depends(get_db)) -> list[Prize]:
    return list(db.scalars(select(Prize).where(Prize.is_active.is_(True)).order_by(Prize.sort_order)))
