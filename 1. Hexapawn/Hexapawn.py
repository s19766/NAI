# Author: Damian Eggert s19766
# Author: Adrian Paczewski s14973
# code reference: https://www.oreilly.com/library/view/artificial-intelligence-with/9781786464392/ch09s10.html
#                 https://github.com/PacktPublishing/Artificial-Intelligence-with-Python/blob/master/Chapter%2009/code/hexapawn.py
# game description: https://pl.wikipedia.org/wiki/Hexapawn

# pip install easyAI
from easyAI import TwoPlayerGame, AI_Player, Human_Player, Negamax


class GameController(TwoPlayerGame):
    def __init__(self, players, size=(4, 4)):
        """
        Define board, players, number of pawns, direction per player

        Parameters:
            players (list): List of players which will play the game

        Returns:
            Self object.
        """
        self.size = size
        num_pawns, len_board = size
        # p = position
        p = [[(i, j) for j in range(len_board)]
             for i in [0, num_pawns - 1]]

        for i, d, goal, pawns in [(0, 1, num_pawns - 1,
                                   p[0]), (1, -1, 0, p[1])]:
            players[i].direction = d
            players[i].goal_line = goal
            players[i].pawns = pawns

        # Define the players
        self.players = players

        # Define who starts first
        self.nplayer = 1
        self.current_player = 1

        # Define the alphabets
        self.alphabets = 'ABCDEFGH'

        # Convert B4 to (1, 3)
        self.to_tuple = lambda s: (self.alphabets.index(s[0]),
                                   int(s[1:]) - 1)

        # Convert (1, 3) to B4
        # [(1, 3), (2, 3)] == B4 C4
        # [(1, 3), (2, 3)] == move[0][0] == 1, move[0][1] + 1 == 4
        # move[0][0] == 1 == alphabets[1] == B
        self.to_string = lambda move: ' '.join([self.alphabets[
                                                    move[i][0]] + str(move[i][1] + 1)
                                                for i in (0, 1)])

    # Define the possible moves
    def possible_moves(self):
        """
        Returns:
            List of possible moves.
        """
        moves = []
        opponent_pawns = self.opponent.pawns
        d = self.player.direction

        for i, j in self.player.pawns:
            if (i + d, j) not in opponent_pawns:
                moves.append(((i, j), (i + d, j)))

            if (i + d, j + 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j + 1)))

            if (i + d, j - 1) in opponent_pawns:
                moves.append(((i, j), (i + d, j - 1)))

        return list(map(self.to_string, [(i, j) for i, j in moves]))

    def make_move(self, move):
        """
        Define how to make a move.

        Parameters:
            move (str): Accepts the player's chosen move, example: "A1 B1"
        """
        move = list(map(self.to_tuple, move.split(' ')))
        ind = self.player.pawns.index(move[0])
        self.player.pawns[ind] = move[1]

        if move[1] in self.opponent.pawns:
            self.opponent.pawns.remove(move[1])

    def loss_condition(self):
        """
        Define when player lose the game.

        If player captures all enemy pawns /
        if player is not able to move any pawn /
        if player get to the goal line.

        Returns:
            Bool: True or False
        """
        return (any([i == self.opponent.goal_line
                     for i, j in self.opponent.pawns])
                or (self.possible_moves() == []))

    # Check if the game is over
    def is_over(self):
        return self.loss_condition()

    # Show the current status
    def show(self):
        """
        Function is printing board, pawns and fields.
        """
        f = lambda x: '1' if x in self.players[0].pawns else (
            '2' if x in self.players[1].pawns else '.')

        print("\n".join([" ".join([f((i, j))
                                   for j in range(self.size[1])])
                         for i in range(self.size[0])]))


if __name__ == '__main__':
    # Compute the score
    scoring = lambda game: -100 if game.loss_condition() else 0

    # Define the algorithm
    algorithm = Negamax(2, scoring)

    # Start the game
    game = GameController([Human_Player(),
                           AI_Player(algorithm)])
    game.play()
    print('\nPlayer', game.current_player, 'wins after', game.nmove, 'turns')
