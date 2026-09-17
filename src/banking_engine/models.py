from abc import ABC, abstractmethod
from typing import Dict, Any
from banking_engine.exceptions import InvalidAmountError, InsufficientFundsError


class Account(ABC):
    """Abstract Base Class demonstrating Encapsulation and Abstraction."""

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative.")
        self.account_id = account_id
        self.owner = owner
        self._balance = float(initial_balance)  # Encapsulated attribute

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive.")
        self._balance += amount
        return self._balance

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """Polymorphic withdrawal logic implemented by subclasses."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self._balance,
            "account_type": self.__class__.__name__,
        }


class SavingsAccount(Account):
    """Savings account with interest rate capabilities."""

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0, interest_rate: float = 0.02):
        super().__init__(account_id, owner, initial_balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError(f"Cannot withdraw {amount}. Available balance: {self._balance}")
        self._balance -= amount
        return self._balance

    def apply_interest(self) -> float:
        interest = self._balance * self.interest_rate
        self._balance += interest
        return self._balance

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data


class CheckingAccount(Account):
    """Checking account supporting an overdraft limit."""

    def __init__(self, account_id: str, owner: str, initial_balance: float = 0.0, overdraft_limit: float = 500.0):
        super().__init__(account_id, owner, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be positive.")
        if self._balance - amount < -self.overdraft_limit:
            raise InsufficientFundsError(
                f"Exceeds overdraft limit of {self.overdraft_limit}. Balance: {self._balance}"
            )
        self._balance -= amount
        return self._balance

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["overdraft_limit"] = self.overdraft_limit
        return data