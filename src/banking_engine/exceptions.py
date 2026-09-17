class BankingEngineError(Exception):
    """Base exception for the banking engine domain."""
    pass


class InvalidAmountError(BankingEngineError):
    """Raised when an operation is attempted with an invalid amount (e.g., negative or zero)."""
    pass


class InsufficientFundsError(BankingEngineError):
    """Raised when withdrawal exceeds available balance or credit limit."""
    pass


class AccountNotFoundError(BankingEngineError):
    """Raised when an account lookup fails."""
    pass