import pytest
import os
from banking_engine.models import SavingsAccount, CheckingAccount
from banking_engine.persistence import BankManager
from banking_engine.exceptions import InvalidAmountError, InsufficientFundsError, AccountNotFoundError


def test_savings_account_deposit_and_withdraw():
    acc = SavingsAccount("S101", "Alice", 100.0)
    assert acc.balance == 100.0
    acc.deposit(50.0)
    assert acc.balance == 150.0
    acc.withdraw(30.0)
    assert acc.balance == 120.0


def test_savings_account_interest():
    acc = SavingsAccount("S102", "Bob", 1000.0, interest_rate=0.05)
    acc.apply_interest()
    assert acc.balance == 1050.0


def test_checking_overdraft():
    acc = CheckingAccount("C101", "Charlie", 100.0, overdraft_limit=200.0)
    acc.withdraw(250.0)  # Allowed due to overdraft
    assert acc.balance == -150.0

    with pytest.raises(InsufficientFundsError):
        acc.withdraw(100.0)  # Exceeds total overdraft capability (-150 - 100 = -250 < -200)


def test_invalid_input_exceptions():
    with pytest.raises(InvalidAmountError):
        SavingsAccount("S103", "Dave", -50.0)

    acc = SavingsAccount("S104", "Eve", 100.0)
    with pytest.raises(InvalidAmountError):
        acc.deposit(-10.0)

    with pytest.raises(InvalidAmountError):
        acc.withdraw(0.0)


def test_json_and_csv_persistence(tmp_path):
    manager = BankManager()
    manager.add_account(SavingsAccount("S201", "Frank", 500.0))
    manager.add_account(CheckingAccount("C201", "Grace", 200.0))

    json_path = tmp_path / "ledger.json"
    csv_path = tmp_path / "ledger.csv"

    # Test JSON save & load
    manager.save_to_json(str(json_path))
    assert os.path.exists(json_path)

    new_manager = BankManager()
    new_manager.load_from_json(str(json_path))
    assert new_manager.get_account("S201").balance == 500.0

    # Test CSV Export
    manager.export_to_csv(str(csv_path))
    assert os.path.exists(csv_path)


def test_missing_account_error():
    manager = BankManager()
    with pytest.raises(AccountNotFoundError):
        manager.get_account("NON_EXISTENT")