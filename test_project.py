from project import Bank, Account


def test_find_account():
    bank = Bank()
    bank.create_account(102,"sayed",1234,100)
    assert bank.find_account(101) is None

    result = bank.find_account(102)
    assert result.account_number == 102

def test_deposit():
    account = Account(101,"sayed",1234,0)
    account.deposit(100)

    assert account.balance == 100

def test_withdrawal():
    account = Account(101,"sayed",1234,100)
    account.withdrawal(50)

    assert account.balance == 50

    account.withdrawal(1000)  
    assert account.balance == 50


