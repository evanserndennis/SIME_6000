import random
import matplotlib.pyplot as plt
from statistics import mean
from game import Game


"""
main.py

Entry point for Eastonoply. Wires together Player, Property, and Game to
run the simulations required by the assignment:

  Part A: Play one game, graph each player's bank account balance over
          time, and report final standings by money.
  Part B: Play 30 games and report the average number of turns Player 1
          took across those games.
  Part C (Grad): Play 100 games under the "last player standing" rules and
          report each player's win probability.

"""


random.seed(42)

# Part A
game = Game()
game.run()

for player in game.players:
    print(f'Player {player.player_id + 1}: ${player.money}')
    plt.plot(range(len(player.balance_history)), player.balance_history, label=f'Player {player.player_id + 1}')

plt.title('Bank Balances During Play of Game')
plt.xlabel('Cash Movement Events')  # Does not equate to turns, cash events can take place for a player during another player's turn
plt.ylabel('Cash Balance')
plt.legend()
plt.show()

# Part B
first_player_turns = []

for i in range(0, 30):  # Range defined by assignment
    game = Game()
    game.run()
    first_player_turns.append(game.players[0].turns)

print(f'\nOn average, Player 1 played {round(mean(first_player_turns), 2)} turns\n')

# Part C (Grad)
C_RANGE_UPPER = 100  # Range defined by assignment

player_wins = {
    "Player 1": 0,
    "Player 2": 0,
    "Player 3": 0,
    "Player 4": 0,
}

for i in range(0, C_RANGE_UPPER):
    game = Game(simplified=False)
    game.run()
    player_wins[f'Player {game.winner.player_id + 1}'] += 1

print(f'Win statistics by player over {C_RANGE_UPPER} runs (Until final elimination):')
for key, value in player_wins.items():
    print(f'{key}: {value} ({round(value / C_RANGE_UPPER, 4) * 100}%)')

