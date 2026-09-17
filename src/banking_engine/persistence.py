import json
import csv
from typing import Dict, List
from banking_engine.models import Account, SavingsAccount, CheckingAccount
from banking_engine.exceptions import AccountNotFoundError


class BankManager:
    """Manages bank accounts and handles file I/O operations."""

    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def add_account(self, account: Account) -> None:
        self.accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Account '{account_id}' not found.")
        return self.accounts[account_id]

    def save_to_json(self, file_path: str) -> None:
        """Saves account ledger state to a JSON file."""
        data = [acc.to_dict() for acc in self.accounts.values()]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, file_path: str) -> None:
        """Loads account ledger state from a JSON file."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.accounts.clear()
        for item in data:
            acc_type = item.get("account_type")
            if acc_type == "SavingsAccount":
                acc = SavingsAccount(
                    item["account_id"], item["owner"], item["balance"], item.get("interest_rate", 0.02)
                )
            elif acc_type == "CheckingAccount":
                acc = CheckingAccount(
                    item["account_id"], item["owner"], item["balance"], item.get("overdraft_limit", 500.0)
                )
            else:
                continue
            self.add_account(acc)

    def export_to_csv(self, file_path: str) -> None:
        """Exports ledger summary to a CSV file."""
        fieldnames = ["account_id", "owner", "balance", "account_type"]
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for acc in self.accounts.values():
                writer.writerow(acc.to_dict())