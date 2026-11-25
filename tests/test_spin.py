import pytest
from app.models import Prize
from app.services.spin import choose_prize


class FixedRandom:
    def __init__(self, value):
        self.value = value

    def randrange(self, total):
        return self.value


def prize(code, weight, active=True):
    return Prize(code=code, name=code, probability_bp=weight, is_active=active, sort_order=0)


def test_weighted_choice_uses_cumulative_ranges():
    prizes = [prize("a", 2500), prize("b", 2000), prize("c", 5500)]
    assert choose_prize(prizes, FixedRandom(0)).code == "a"
    assert choose_prize(prizes, FixedRandom(2499)).code == "a"
    assert choose_prize(prizes, FixedRandom(2500)).code == "b"
    assert choose_prize(prizes, FixedRandom(9999)).code == "c"


def test_zero_probability_prize_is_never_eligible():
    prizes = [prize("zero", 0), prize("winner", 10000)]
    assert choose_prize(prizes, FixedRandom(0)).code == "winner"


def test_inactive_prize_is_ignored():
    prizes = [prize("inactive", 10000, active=False)]
    with pytest.raises(ValueError):
        choose_prize(prizes, FixedRandom(0))
