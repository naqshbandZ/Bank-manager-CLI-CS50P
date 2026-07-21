CLI Bank

Video Demo: <URL HERE>

Description:

CLI Bank is a command-line banking application written in Python for my CS50P final project. It lets a user create a bank account, log in with an account number and PIN, and then deposit money, withdraw money, check their balance, and view a full history of past transactions. All account and transaction data is stored permanently in CSV files, so information is never lost between runs of the program — you can close the program and reopen it later, and your account, balance, and transaction history will still be there exactly as you left them.

The project is built around three classes: Bank, Account, and Transaction.

The Bank class manages the overall collection of accounts. It is responsible for creating new accounts, searching for an existing account by account number, and saving or loading all customer data to and from customers.csv. This file acts as a permanent "snapshot" of every account and its current balance. Every time an account is created or its balance changes, customers.csv is fully rewritten with the latest information for every account currently in the program, so the file is always an accurate, up-to-date record.

The Account class represents a single bank account and holds its account number, owner name, PIN, current balance, and a list of transactions made during the current session. It has methods to deposit money, withdraw money (with a check to prevent withdrawing more than the current balance), and save its transactions to its own dedicated file, named transactions_<account_number>.csv. Each account has its own transaction file so that transaction history stays organized per customer and doesn't mix between accounts. After every deposit or withdrawal is saved to file, the in-memory transaction list is cleared, which prevents the same transaction from being written to the file more than once on a later save.

The Transaction class is a small data class that stores the type of transaction (deposit or withdrawal), the amount, the date it occurred, and the resulting balance at that point in time. It has a custom __str__ method so that individual transactions can be printed in an easy-to-read format if needed.

The main() function ties everything together into an interactive command-line menu. When the program starts, it loads any existing customer data from customers.csv. The user is then shown a menu to create a new account, log in to an existing one, or exit the program. When creating an account, the program checks that the chosen account number isn't already taken before allowing the account to be created, and validates that all numeric fields are actually numbers, re-prompting the user if not. When logging in, the program checks the account number and PIN together; if they don't match a real account, the user is asked to try again or told to register first.

Once logged in, the user reaches a second menu where they can view their current balance, make a deposit, make a withdrawal, view their transaction history, or log out. Deposits and withdrawals are validated so that negative amounts are rejected, and withdrawals larger than the current balance are refused. Transaction history is read directly from the account's CSV file and displayed as a clean, readable table using the tabulate library, with dollar signs added to amount and balance columns for clarity. Various messages throughout the program — errors, successes, and login feedback — are shown using the cowsay library, which prints messages inside a small speech bubble next to an ASCII cat, giving the CLI a more lighthearted, friendly feel instead of plain text output.

I chose to persist data using CSV files rather than a database because CSV is simple, human-readable, and doesn't require any extra setup, which fit the scope of a CS50P final project well. I separated customer data and transaction data into different files because they serve different purposes: customers.csv only ever needs to reflect the current state of each account, so it makes sense to overwrite it completely on every save, while each account's transaction file is a permanent, ever-growing log, so it only ever has new lines appended to it, never erased.

One of the more interesting challenges while building this project was making sure that balances persisted correctly across separate runs of the program, rather than resetting or duplicating on each save. This required understanding the difference between updating a value in memory versus actually writing it to disk, and being careful about when to save, when to load, and when to clear temporary data so that it wouldn't be saved twice.

Files


project.py — contains the Bank, Account, and Transaction classes, along with main(), which runs the interactive CLI menu.
test_project.py — contains unit tests for Bank.find_account(), Account.deposit(), and Account.withdrawal(), using assert statements to check both normal and edge-case behavior (such as searching for a non-existent account or withdrawing more than the available balance).
requirements.txt — lists the external Python packages required to run the project (tabulate, cowsay, and pytest for running the tests).
customers.csv — generated automatically the first time the program runs; stores the current account number, name, PIN, and balance for every customer.
transactions_<account_number>.csv — generated automatically the first time an account makes a deposit or withdrawal; stores the full transaction history for that specific account.


How to run

pip install -r requirements.txt
python project.py

How to test

pytest test_project.py
