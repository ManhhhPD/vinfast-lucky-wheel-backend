from datetime import datetime

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prize(Base):
    __tablename__ = "prizes"
    __table_args__ = (CheckConstraint("probability_bp >= 0", name="ck_prizes_probability_nonnegative"),)

    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    probability_bp: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class SpinResult(Base):
    __tablename__ = "spin_results"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    player_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(30), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    prize_code: Mapped[str] = mapped_column(ForeignKey("prizes.code"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    client_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    prize: Mapped[Prize] = relationship()
