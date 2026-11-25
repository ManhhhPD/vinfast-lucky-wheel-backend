from pydantic import BaseModel, Field, field_validator


class PrizeResponse(BaseModel):
    code: str
    name: str
    probability_bp: int
    sort_order: int
    model_config = {"from_attributes": True}


class SpinRequest(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=100, strict=True)

    phone_number: str = Field(default='', max_length=30, strict=True)
    address: str = Field(default='', max_length=500, strict=True)

    @field_validator("player_name", "phone_number", "address", mode="before")
    @classmethod
    def trim_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class SpinResponse(BaseModel):
    prize_code: str
    prize_name: str
    spin_id: int
