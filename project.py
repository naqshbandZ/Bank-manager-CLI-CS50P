from datetime import date
import csv
from tabulate import tabulate
import sys
import os
import cowsay


class Bank:
    def __init__(self):
        self.accounts = []

    def create_account(self,account_number,name,pin,balance):
        account = Account(account_number,name,pin,balance)
        self.accounts.append(account)

    def find_account(self,user):
        for account in self.accounts:
            if user == account.account_number:
                return account
        return None


    def save_customers(self):
        with open("customers.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["account_number", "name", "pin", "balance"])
            for account in self.accounts:
                writer.writerow([account.account_number,account.name,account.pin,account.balance])

    def load_customers(self):
        if not os.path.exists("customers.csv"):
            with open("customers.csv", "w") as fl:
                writer = csv.writer(fl)
                writer.writerow(["account_number","name","pin","balance"])
                return

        with open("customers.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for read in reader:
                account = Account(int(read[0]),read[1],int(read[2]),int(read[3]))
                self.accounts.append(account)



class Account:
    def __init__(self,account_number,name,pin,balance=0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def save_transaction(self):
        filename = f"transactions_{self.account_number}.csv"
        with open(filename, "a") as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["type","amount","date","balance"])

            for transaction in self.transactions:
                writer.writerow([transaction.type,transaction.amount,transaction.date,transaction.balance])


    def deposit(self,amount):
        self.balance += amount
        today = date.today()
        transaction = Transaction("deposit", amount, today, self.balance)

        self.transactions.append(transaction)
        cowsay.cow("Successfully deposit ")

    def withdrawal(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            cowsay.cow("Successfully withdrawal ")
            today = date.today()
            transaction = Transaction("withdrawal", amount, today, self.balance)

            self.transactions.append(transaction)
        else:
            cowsay.cow("No balance")

class Transaction:
    def __init__(self,type,amount,date,balance):
        self.type = type
        self.amount = amount
        self.date = date
        self.balance = balance

    def __str__(self):
        return f"Type: {self.type} Amount: {self.amount} Date: {self.date}  Balance: {self.balance}$"


def main():
    bank = Bank()
    bank.load_customers()
    while True:
        print("=" * 42)
        print("        WELCOME TO CLI BANK")
        print("=" * 42)
        print()
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print()
        try:

            choice = int(input("Choose an option: "))
            print()
            print("=" * 42)
            print("=" * 42)

        except ValueError:
            cowsay.cow("please choice from numbers!")
            continue


        if choice == 1:
            name = input("Account holder Name: ")
            try:
                while True:
                    account_number = int(input("Account number: "))
                    if bank.find_account(account_number) is not None:
                        cowsay.cow("Account number has already taken!")
                    else:
                        break
                balance = int(input("Starting balance: "))
                pin = int(input("Pincode: "))
            except ValueError:
                cowsay.cow("ACCOUNT NUMBER, PIN AND BALANCE SHUOLD BE DIGITS!")
                continue
            bank.create_account(account_number,name,pin,balance)
            bank.save_customers()
            print()
            cowsay.cow(f"Account {name} created successfully!")

        elif choice == 2:
            while True:
                user = int(input("Account Number: "))
                passcode = int(input("Passcode: "))
                account = bank.find_account(user)
                if account:
                    if passcode == account.pin:
                        while True:
                            try:
                                print("=" * 42)
                                print(f"        | Welcome {account.name} |")
                                print("=" * 42)
                                print()
                                print(" 1. Show balance")
                                print(" 2. Deposit")
                                print(" 3. Withdrawal")
                                print(" 4. Show transactions")
                                print(" 5. Logout")
                                print()
                                print("=" * 42)
                                print()
                                user_choice = int(input("Choose: "))
                                if user_choice == 1:
                                    print(tabulate([[f"{account.balance}$"]], headers=["Balance"], tablefmt="grid"))
                                    print()

                                elif user_choice == 5:
                                    sys.exit(cowsay.cow(f"GOOD BYE {account.name}"))
                                elif user_choice == 2:
                                    try:
                                        amount = int(input("Amount: "))
                                        if amount < 0:
                                            cowsay.cow("cannot deposit")
                                        else:
                                            account.deposit(amount)
                                            account.save_transaction()
                                            account.transactions.clear()
                                            bank.save_customers()

                                    except ValueError:
                                        cowsay.cow("should be digits")

                                elif user_choice == 3:
                                    try:
                                        withd = int(input("Amount: "))
                                        account.withdrawal(withd)
                                        account.save_transaction()
                                        account.transactions.clear()
                                        bank.save_customers()
                                    except ValueError:
                                        cowsay.cow("should be digits!")

                                elif user_choice == 4:

                                    filenam = f"transactions_{account.account_number}.csv"
                                    if not os.path.exists(filenam):
                                        cowsay.cow("NO TRSANSACTIONS")
                                        print()
                                    else:
                                        with open(filenam, "r") as file:
                                            reader = csv.reader(file)

                                            next(reader)
                                            data = []
                                            for read in reader:
                                                read[1] = f"{read[1]}$"
                                                read[3] = f"{read[3]}$"
                                                data.append(read)
                                                headers = ["Type", "Amount", "Date", "Balance"]
                                            print(tabulate(data, headers=headers, tablefmt="grid"))
                                            print()
                            except ValueError:
                                cowsay.cow("you have to choose from 1 to 5")
                                print()
                                continue
                    else:
                        cowsay.cow("Wrong passcode")
                        print()
                        break
                else:
                    cowsay.cow("Register !")

        elif choice == 3:
            sys.exit(cowsay.cow("GOOD BYE"))

        else:
            cowsay.cow("Invalid option, choose 1-3")




if __name__ == "__main__":
    main()
