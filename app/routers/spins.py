from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Prize, SpinResult
from app.schemas import SpinRequest, SpinResponse
from app.services.spin import choose_prize

router = APIRouter(prefix="/api/spins", tags=["spins"])


@router.post("", response_model=SpinResponse, status_code=201)
def create_spin(payload: SpinRequest, request: Request, db: Session = Depends(get_db)) -> SpinResponse:
    prizes = list(db.scalars(select(Prize).where(Prize.is_active.is_(True)).order_by(Prize.sort_order)))
    try:
        prize = choose_prize(prizes)
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    result = SpinResult(
        player_name=payload.player_name,
        phone_number=payload.phone_number,
        address=payload.address,
        prize_code=prize.code,
        client_ip=request.client.host if request.client else None,
    )
    try:
        db.add(result)
        db.commit()
        db.refresh(result)
    except Exception:
        db.rollback()
        raise
    return SpinResponse(prize_code=prize.code, prize_name=prize.name, spin_id=result.id)
