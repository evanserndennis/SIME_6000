from property import Property
from player import Player
import random

class Game:
    def __init__(self, winner=None, player_count=4, property_count=40, turn=0, simplified=True):
        self.winner = winner
        self.player_count = player_count
        self.property_count = property_count
        self.turn = turn
        self.simplified = simplified
        self._generate_board()
        self._generate_players()

    def _dice_roll(self):
        return random.randint(1,6) + random.randint(1,6)

    def _generate_board(self):
        self.properties = []
        for property in range(0,self.property_count):
            self.properties.append(Property(property_id=property))

    def _generate_players(self):
        self.players = []
        for player in range(0,self.player_count):
            self.players.append(Player(player_id=player))

    def _game_over(self):
        if self.simplified:
            return any(not player.alive for player in self.players)
        else:
            return sum(player.alive for player in self.players) == 1

    def _set_winner(self):
        if not self.simplified:
            for player in self.players:
                if player.alive:
                    self.winner = player

    def run(self):
        while not self._game_over():
            current = self.players[self.turn % self.player_count]
            self.turn += 1

            if not current.alive:
                continue

            else:
                current.turns += 1
                dice_roll = self._dice_roll()

                if current.position + dice_roll >= self.property_count:
                    current.add_money(2)

                current.position = (current.position + dice_roll) % self.property_count
                property = self.properties[current.position]

                if property.owner is None:
                    if current.money >= 3:
                        property.owner = current
                        current.properties.append(property)
                        current.add_money(-3)

                elif property.owner == current:
                    property.rent += 1

                elif current.money >= property.rent:
                    current.add_money(-property.rent)
                    property.owner.add_money(property.rent)

                else:
                    property.owner.add_money(current.money)
                    current.add_money(-current.money)  # Transfers remaining balance to landlord so that eliminated players cash is always zero
                    current.alive = False
                    if not self.simplified:
                        for property in current.properties:
                            property.rent = 1
                            property.owner = None
                        current.properties.clear()

        self._set_winner() 

