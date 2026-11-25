from app.schemas import SpinRequest


def test_spin_request_trims_name():
    assert SpinRequest(player_name="  Lan  ").player_name == "Lan"


def test_spin_request_rejects_blank_name():
    try:
        SpinRequest(player_name="   ")
    except ValueError:
        return
    raise AssertionError("blank names should be rejected")
