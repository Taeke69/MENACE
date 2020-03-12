#import numpy as np
import random
#from time import sleep

class State:
    def __init__(self, player1, player2):
        self.state = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.player1 = player1
        self.player2 = player2

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
        #print(moves)
        return moves


    def play_move(self, position, mark):
        self.state[position] = mark

    def validate_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False
        if 0 <= move < 9 and self.state[move] == ' ':
            return True
        else:
            return False

    def get_player(self):
        count_x = 0
        count_o = 0
        for mark in self.state:
            if mark == self.player1.mark:
                count_x += 1
            if mark == self.player2.mark:
                count_o += 1
        return (self.player2 if count_x > count_o else self.player1)

    def check_winner(self):
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
        #print('Menace state', state.get_state())
        state_s = str(state.get_state())
        if state_s not in self.known_states:
            #new_choice = moves

            state_c = state
            bestScore = -2
            bestMove = -1
            for x in moves:
                print(x)
                state_c.play_move(x, self.mark)
                score = minimax(state_c, state_c.get_moves(), False, 0)
                state_c.play_move(x, ' ')
                if (score > bestScore):
                    bestScore = score
                    bestMove = x
                    print('score', score)
                    print('x', x)
            
            new_choice = bestMove

            self.known_states[state_s] = new_choice
            #self.known_states[state_s] = new_choice * (len(new_choice) // 2 + 1)
            print('new situation', self.known_states[state_s])
            
        print('known_state', self.known_states[state_s])
        choices = self.known_states[state_s]
        print('choices', choices)
        choice = choices
        #if len(choices):
            #choice = random.choice(choices)
            #choice = minimax(state, choices, self)
            # state_c = state
            # bestScore = -2
            # bestMove = -1
            # for x in choices:
            #     state_c.play_move(x, self.mark)
            #     score = minimax(state_c, state_c.get_moves(), False, 0)
            #     state_c.play_move(x, ' ')
            #     if (score > bestScore):
            #         bestScore = score
            #         bestMove = x
            
            # choice = bestMove

        self.moves_played.append((state_s, choice))
        print('moves played', self.moves_played)
        #else:
            #choice = -1
        print('choice', choice)
        return choice

    def end_game(self, winner):
        if (not winner):
            self.draw_game()
            return
        if (winner == self.mark):
            self.win_game()
            return
        else:
            self.lose_game()
            return

    def win_game(self):
        print('w')
        for (state, choice) in self.moves_played:
            self.known_states[state].append([choice, choice, choice])
        self.wins += 1

    def draw_game(self):
        print('d')
        for (state, choice) in self.moves_played:
            self.known_states[state].append(choice)
        self.draws += 1
    
    def lose_game(self):
        print('l')
        for (state, choice) in self.moves_played:
            #print(self.known_states[state])
            known_state = self.known_states[state]
            #print('known_state', known_state)
            del known_state[known_state.index(choice)]
            #print(self.known_states[state])
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
            pass
            

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
    
    def end_game(self, winner):
        if (not winner):
            print("Draw...")
            return
        if (winner == self.mark):
            print("Congratulations! You won!")
            return
        else:
            print("Lmao, you suck.")
            return

def minimax(state, moves, isMaxPlayer, depth):
    winner = state.check_winner()
    if (winner):
        if isMaxPlayer:
            return -1
        elif not isMaxPlayer:
            return 1
    if (len(moves) < 1 or depth == 10):
        return 0

    if isMaxPlayer:
        bestScore = -2
        for move in moves:
            state.play_move(move, state.get_player().mark)
            score = minimax(state, state.get_moves(), False, depth+1)
            state.play_move(move, ' ')
            if (score > bestScore):
                bestScore = score
        
        #print('maxscore', bestScore)
        return bestScore

    else:
        bestScore = 2
        for move in moves:
            state.play_move(move, state.get_player().mark)
            score = minimax(state, state.get_moves(), True, depth+1)
            state.play_move(move, ' ')
            if (score < bestScore):
                bestScore = score
                
        #print('minscore', score)    
        return bestScore


def play_game(player1, player2):
    state = State(player1, player2)
    player1.start_game()
    player2.start_game()
    while True:
        print(state.get_state())
        current_player = state.get_player()
        moves = state.get_moves()
        move = current_player.get_move(state, moves)
        state.play_move(move, current_player.mark)
        print(state.check_winner())
        winner = state.check_winner()
        if (winner or len(moves) - 1 < 1):
            print('WINNER', winner)
            #player1.end_game(winner)
            #player2.end_game(winner)
            return;
        # if (winner):
        #     player1.end_game()
        #     player2.end_game()
        #     print(state.get_state())
        #     print("Congratulations! %s won the round!" % state.check_winner())
        #     player2.lose_game()
        #     return;
        # if (len(moves) - 1 < 1):
        #     print(state.get_state())
        #     print("Draw!")
        #     return

if __name__ == '__main__':
    player1 = Player('X')
    player2 = Menace('O')
    while True:
        print("\n\nStarting new game: ")
        play_game(player1, player2)
        print("\n\nStarting new game: ")
        play_game(player2, player1)