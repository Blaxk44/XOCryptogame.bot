user_balances = {}

def get_balance(user_id):
    return user_balances.get(user_id, 0)

def deposit(user_id, amount):
    current = get_balance(user_id)
    user_balances[user_id] = current + amount

def withdraw(user_id, amount):
    current = get_balance(user_id)
    if current >= amount:
        user_balances[user_id] = current - amount
        return True
    return False
