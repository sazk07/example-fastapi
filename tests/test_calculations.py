import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

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

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100

def test_bank_default_amount(zero_bank_account):
    assert bank_account.balance == 0

def test_bank_withdraw():
    bank_account = BankAccount(100)
    bank_account.withdraw(20)
    assert bank_account.balance == 80

def test_bank_deposit():
    bank_account = BankAccount(100)
    bank_account.deposit(20)
    assert bank_account.balance == 120

def test_collect_interest():
    bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert bank_account.balance == 100*1.1