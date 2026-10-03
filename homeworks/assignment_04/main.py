from player import Player
from pathlib import Path
import matplotlib.pyplot as plt


PLAYER_METADATA_PATH = Path(__file__).resolve().parent / 'player_names.csv'
PLAYER_STATS_PATH = Path(__file__).resolve().parent / '10000AtBats.csv'

SCORING_MATRIX = {
    # -2.0 Points
    'Grounded Into DP': -2.0,
    # -1.0 Points
    'Strikeout': -1.0,
    # -0.5 Points
    'Flyout': -0.5,
    'Groundout': -0.5,
    'Forceout': -0.5,
    'Pop Out': -0.5,
    'Lineout': -0.5,
    'Double Play': -0.5,
    'Bunt Groundout': -0.5,
    # +0.5 Points
    'Walk': 0.5,
    'Intent Walk': 0.5,
    'Hit By Pitch': 0.5,
    # +1.0 Points
    'Single': 1.0,
    'Sac Fly': 1.0,
    'Sac Bunt': 1.0,
    # +2.0 Points
    'Double': 2.0,
    # +3.0 Points
    'Triple': 3.0,
    # +5.0 Points
    'Home Run': 5.0
}

player_data = []

with open(PLAYER_METADATA_PATH, 'r') as metadata_file:
    records = metadata_file.readlines()[1:]
    for record in records:
        split_record = record.strip().split(',')
        player_data.append(Player(
            player_id=split_record[0],
            player_name=f'{split_record[2]}, {split_record[1]}'
            ))

with open(PLAYER_STATS_PATH, 'r') as stats_file:
    at_bats = stats_file.readlines()[1:]
    for player in player_data:
        for at_bat in at_bats:
            split_at_bat = at_bat.strip().split(',')
            player_id = split_at_bat[5]
            event = split_at_bat[9]
            if player_id == player.player_id:
                player.player_history.append(event)
        player.generate_scoring_history(scoring_matrix=SCORING_MATRIX)

# Filtering players with less than 25 items in their history
filtered_players = filter(lambda player: len(player.scoring_history)>=25, player_data)

# Sorting players by score and pulling the top/bottom three
sorted_players = sorted(filtered_players, key=lambda player: player.average_history[-1], reverse=True)
top_players = sorted_players[:3]
bottom_players = sorted_players[-3:]

print('\nTop players:')
for player in top_players:
    print(f'\t{player.player_name}: {player.average_history[-1]:.2f} pts')
    plt.plot(
        range(0,len(player.scoring_history)),
        player.average_history,
        label=player.player_name
    )

print('\nBottom players:')
for player in bottom_players:
    print(f'\t{player.player_name}: {player.average_history[-1]:.2f} pts')

plt.legend()
plt.show()