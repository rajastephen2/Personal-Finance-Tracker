class Account:
    def __init__(self):
        self.balance = 0
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        if transaction.type == "income":
            self.balance += transaction.amount
        else:
            self.balance -= transaction.amount

    def get_balance(self):
        return self.balance