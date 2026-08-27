import random


'''
Lecture 02: Craps

Note: I already know Python fairly well, so this exercise was elementary
for me. I didn't closely follow along during lecture, but this should be
enough to be ready for next lecture's material.
'''

random.seed(42) # Seeding the file for the purposes of this lecture

def _die_roll():
    return random.randint(1,6)

def _come_out_roll(budget: int) -> int:
    while True:
        try:
            bet = int(input('How many chips would you like to bet?\n' \
            '\t(Integers only please):'))
        except ValueError:
            print('Please enter a whole number.')
            continue

        if bet <= 0:
            print('Bet must be greater than 0.')
        elif bet > budget:
            print(f'You only have {budget} chips.')
        else:
            break

    die1 = _die_roll()
    die2 = _die_roll()
    dice_roll = die1 + die2
    print(f'Come-out roll: {die1} + {die2} = {dice_roll}')

    match dice_roll:
        case 7 | 11:
            print(f'Natural! You win {bet} chips.')
            return bet
        case 2 | 3 | 12:
            print(f'Craps! You lose {bet} chips.')
            return -bet
        case _:
            print(f'Point established: {dice_roll}')
            if _play_point(dice_roll):
                print(f'You made the point! You win {bet} chips.')
                return bet
            else:
                print(f'Seven out. You lose {bet} chips.')
                return -bet

    return False


def _play_point(point: int) -> bool:
    playing = True

    while playing:
        die1 = _die_roll()
        die2 = _die_roll()
        dice_roll = die1 + die2
        print(f'  Rolled: {die1} + {die2} = {dice_roll}')

        match dice_roll:
            case _ if dice_roll == point:
                return True
            case 7:
                return False


def _play_game():
    while True:
        try:
            budget = int(input('How many chips would you like to purchase?\n' \
            '\t(Integers only please):'))
        except ValueError:
            print('Please enter a whole number.')
            continue

        if budget <= 0:
            print('Budget must be greater than 0.')
        else:
            break

    print(f'Starting budget: {budget} chips\n')

    while budget > 0:
        budget += _come_out_roll(budget)
        print(f'Current budget: {budget} chips\n')

    print('Out of chips. Game over.')
    return None

if __name__ == '__main__':
    _play_game()