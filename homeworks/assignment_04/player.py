from numpy import mean


class Player:
    def __init__(
            self,
            player_id: str,
            player_name: str,
            player_history=None,
            scoring_history=None,
            average_history=None,
            score=0
        ):
        self.player_id = player_id
        self.player_name = player_name
        self.player_history = player_history if player_history is not None else []
        self.scoring_history = scoring_history if scoring_history is not None else []
        self.average_history = average_history if average_history is not None else []
        self.score = score


    def generate_scoring_history(self, scoring_matrix):
        for record in self.player_history:
            self.scoring_history.append(scoring_matrix.get(record,0))
            self.average_history.append(mean(self.scoring_history))
        self.score = sum(self.scoring_history)

