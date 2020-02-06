#import numpy as np
import random
#from time import sleep

class State:
    def __init__(self):
        self.state = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

    def get_state(self):
        return("\n 0 | 1 | 2 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 3 | 4 | 5 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 6 | 7 | 8 \t  %s | %s | %s \n" % 
                (self.state[0], self.state[1], self.state[2],
                self.state[3], self.state[4], self.state[5],
                self.state[6], self.state[7], self.state[8]))

    def get_moves(self):
        moves = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                moves.append(i)
        print(moves)
        return moves


    def play_move(self, position, player):
        self.state[position] = player

    def validate_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False
        if 0 <= move < 9 and self.state[move] == ' ':
            return True
        else:
            return False

    def get_player(self, player1, player2):
        count_x = 0
        count_o = 0
        for mark in self.state:
            if mark == 'X':
                count_x += 1
            if mark == 'O':
                count_o += 1
        return (player2 if count_x > count_o else player1)

    def check_winner(self):
        # return((self.board[0] != ' ' and ((self.board[0] == self.board[1] == self.board[2]) or
        #                                     (self.board[0] == self.board[3] == self.board[6]) or
        #                                     (self.board[0] == self.board[4] == self.board[8])))
        #         or (self.board[4] != ' ' and (self.board[3] == self.board[4] == self.board[5]) or
        #                                     (self.board[1] == self.board[4] == self.board[7]) or
        #                                     (self.board[2] == self.board[4] == self.board[6]))
        for r in range(3):
            if (self.state[r*3] == self.state[r*3+1] == self.state[r*3+2] != ' '):
                return self.state[r*3]
        for c in range(3):
            if (self.state[0+c] == self.state[3+c] == self.state[6+c] != ' '):
                return self.state[0+c]
        if (self.state[0] == self.state[4] == self.state[8] != ' '):
            return self.state[0]
        if (self.state[2] == self.state[4] == self.state[6] != ' '):
            return self.state[2]
        return False

class Menace:
    def __init__(self, mark):
        self.mark = mark
        self.known_states = {}
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def start_game(self):
        self.moves_played = []

    def get_move(self, state, moves):
        if state not in self.known_states:
            new_choice = moves
            self.known_states[state] = new_choice * (len(new_choice) // 2 + 1)
            
        choices = self.known_states[state]
        if len(choices):
            choice = random.choice(choices)
            self.moves_played.append((state, choice))
            print(self.moves_played)
        else:
            choice = -1
        return choice

    def win_game(self):
        for (state, choice) in self.moves_played:
            self.known_states[state].append([choice, choice, choice])
        self.wins += 1

    def draw_game(self):
        for (state, choice) in self.moves_played:
            self.known_states[state].append(choice)
        self.draws += 1
    
    def lose_game(self):
        for (state, choice) in self.moves_played:
            print(self.known_states[state])
            known_state = self.known_states[state]
            del known_state[known_state.index(choice)]
            print(self.known_states[state])
        self.losses += 1

class MonteCarlo:
    def __init__(self, mark):
        self.mark = mark

    def start_game(self):
        pass

    def get_move(self, state, moves):
        return move

    def mc_trial(self, state, player, moves):
        while True:
            current_player = state.get_player(player1, player2)
            moves = state.get_moves()
            random_choice = random.choice(moves)
            state.play_move(random_choice, current_player.mark)

            if (state.check_winner() or len(moves - 1 < 1)):
                return

    def mc_update_scores(self, scores, board, player):
        if (not state.check_winner()):
            for score in scores:
                pass
        else:
            

class Player:
    def __init__(self, mark):
        self.mark = mark
    
    def start_game(self):
        pass

    def get_move(self, state, moves):
        move = input("Enter a move(%s): " % moves)
        while (not state.validate_move(move)):
            move = input("Invalid move, try again: ")
        return int(move)

def play_game(player1, player2):
    state = State()
    player1.start_game()
    player2.start_game()
    while True:
        print(state.get_state())
        current_player = state.get_player(player1, player2)
        moves = state.get_moves()
        move = current_player.get_move(state, moves)
        state.play_move(move, current_player.mark)
        if (state.check_winner()):
            print(state.get_state())
            print("Congratulations! %s won the round!" % state.check_winner())
            player2.lose_game()
            return;
        if (len(moves) - 1 < 1):
            print(state.get_state())
            print("Draw!")
            return

if __name__ == '__main__':
    player1 = Player('X')
    player2 = Menace('O')
    while True:
        print("Starting new game: ")
        play_game(player1, player2)