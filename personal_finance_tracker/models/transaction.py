class Transaction:
    def __init__(self, username, t_type, category, amount, date):
        self.username = username
        self.type = t_type
        self.category = category
        self.amount = amount
        self.date = date

    def to_dict(self):
        return {
            "username": self.username,
            "type": self.type,
            "category": self.category,
            "amount": self.amount,
            "date": self.date
        }