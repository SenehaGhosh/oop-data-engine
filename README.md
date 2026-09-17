# Banking Ledger OOP Data Engine

An object-oriented data management engine modeling a real-world Banking Ledger system. Demonstrates encapsulation, inheritance, polymorphism, custom exception handling, and persistence.

## Features
* **OOP Architecture**: Abstract base class (`Account`) with `SavingsAccount` and `CheckingAccount` subclasses.
* **Custom Exceptions**: Specialized exceptions for balance/amount validation and lookup failures.
* **Persistence**: Dual JSON and CSV serialization support.
* **Unit Testing**: Pytest suite ensuring high test coverage.

## Installation & Running Tests

1. Set up a virtual environment and install test tools:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install pytest pytest-cov