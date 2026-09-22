

class Player:
    def __init__(self, player_id, money=100, balance_history=None, position=0, properties=None, turns=0, alive=True):
        self.player_id = player_id
        self.position = position
        self.properties = properties if properties is not None else []
        self.money = money
        self.balance_history = balance_history if balance_history is not None else [self.money]
        self.turns = turns
        self.alive = alive

    def add_money(self, amount):
        self.money += amount
        self.balance_history.append(self.money)

