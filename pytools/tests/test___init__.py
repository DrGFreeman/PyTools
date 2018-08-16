import pytest
from pytools import constrain

def test_constrain():
    assert constrain(12, 4, 8) == 8
    assert constrain(2, 4, 8) == 4
    assert constrain(6, 4, 8) == 6
    with pytest.raises(ValueError) as e_info:
        constrain(6, 8, 4)
