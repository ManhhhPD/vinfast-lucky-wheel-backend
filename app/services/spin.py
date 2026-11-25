import secrets
from collections.abc import Sequence

from app.models import Prize


def choose_prize(prizes: Sequence[Prize], rng: secrets.SystemRandom | None = None) -> Prize:
    eligible = [prize for prize in prizes if prize.is_active and prize.probability_bp > 0]
    total = sum(prize.probability_bp for prize in eligible)
    if not total:
        raise ValueError("Không có phần thưởng hợp lệ để quay")

    randomizer = rng or secrets.SystemRandom()
    ticket = randomizer.randrange(total)
    cursor = 0
    for prize in eligible:
        cursor += prize.probability_bp
        if ticket < cursor:
            return prize
    raise RuntimeError("Không thể chọn phần thưởng")
