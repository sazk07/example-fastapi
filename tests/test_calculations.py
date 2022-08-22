import pytest
from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize(
    "number_1, number_2, expected", [(3, 2, 5), (7, 1, 8), (12, 4, 16)]
)
def test_add(number_1,number_2, expected):
    print("Testing add function")
    assert add(number_1, number_2) == expected


def test_subtract():
    assert subtract(9, 3) == 6


def test_multiply():
    assert multiply(2, 6) == 12


def test_divide():
    assert divide(20, 4) == 5
