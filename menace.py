#import numpy as np
import random
#from time import sleep

class State:
    def __init__(self, player1, player2):
        self.state = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.player1 = player1
        self.player2 = player2
        self.rotations = [
            [0,1,2,3,4,5,6,7,8],
            [0,3,6,1,4,7,2,5,8],
            [2,5,8,1,4,7,0,3,6],
            [2,1,0,5,4,3,8,7,6],
            [8,7,6,5,4,3,2,1,0],
            [8,5,2,7,4,1,6,3,0],
            [6,3,0,7,4,1,8,5,2],
            [6,7,8,3,4,5,0,1,2]
        ]

    def get_state(self):
        return("\n 0 | 1 | 2 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 3 | 4 | 5 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 6 | 7 | 8 \t  %s | %s | %s \n" % 
                (self.state[0], self.state[1], self.state[2],
                self.state[3], self.state[4], self.state[5],
                self.state[6], self.state[7], self.state[8]))

    def get_string(self):
        return str(self.state)

    def get_moves(self):
        moves = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                moves.append(i)
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

    def get_rotations(self):
        state_rotations = []
        for rotation in self.rotations:
            x = []
            for i in rotation:
                x.append(self.state[i])
            state_rotations.append(str(x))
        return state_rotations

    def unrotate_move(self, rotation, move):
        return self.rotations[rotation][move]

    def check_winner(self):
        for r in range(3):
            if (self.state[r*3] == self.state[r*3+1] == self.state[r*3+2] != ' '):
                return self.player1 if self.player1.mark == self.state[r*3] else self.player2
        for c in range(3):
            if (self.state[0+c] == self.state[3+c] == self.state[6+c] != ' '):
                return self.player1 if self.player1.mark == self.state[0+c] else self.player2
        if (self.state[0] == self.state[4] == self.state[8] != ' '):
            return self.player1 if self.player1.mark == self.state[0] else self.player2
        if (self.state[2] == self.state[4] == self.state[6] != ' '):
            return self.player1 if self.player1.mark == self.state[2] else self.player2
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
        state_s = state.get_string()

        # board rotations
        # [0,1,2,3,4,5,6,7,8] rotation 0
        # [0,3,6,1,4,7,2,5,8] rotation 1
        # [2,5,8,1,4,7,0,3,6] rotation 2
        # [2,1,0,5,4,3,8,7,6] rotation 3
        # [8,7,6,5,4,3,2,1,0] rotation 4
        # [8,5,2,7,4,1,6,3,0] rotation 5
        # [6,3,0,7,4,1,8,5,2] rotation 6
        # [6,7,8,3,4,5,0,1,2] rotation 7

        rotations = state.get_rotations()
        known_rotations = [rotation in self.known_states for rotation in rotations]

        rotation_index = -1

        for i in range(len(known_rotations)):
            if known_rotations[i]:
                rotation_index = i

        if rotation_index == -1:
            rotation_index = 0
            state_c = state
            bestScore = -2
            bestMove = []
            for x in moves:
                print(x)
                state_c.play_move(x, self.mark)
                score = minimax(state_c, state_c.get_moves(), False, 0)
                state_c.play_move(x, ' ')
                if (score == bestScore):
                    bestScore = score
                    #bestMove = x
                    bestMove.append(x)
                elif (score > bestScore):
                    del bestMove[:]
                    bestScore = score
                    bestMove.append(x)
                    print('score', score)
                    print('x', x)
            
            new_choice = bestMove

            self.known_states[state_s] = new_choice
            print('new situation', self.known_states[state_s])

        state_r = rotations[rotation_index]
        print('known_state', self.known_states[state_r])
        choices = self.known_states[state_r]
        print('choices', choices)
        choice = choices
        if len(choices):
            choice = random.choice(choices)
        else:
            del self.known_states[state_r]
            choice = self.get_move(state, state.get_moves())
        self.moves_played.append((state_r, choice))
        choice = state.unrotate_move(rotation_index, choice)

        return choice

    def end_game(self, winner):
        if (not winner):
            self.draw_game()
            return
        if (winner == self):
            self.win_game()
            return
        else:
            self.lose_game()
            return

    def win_game(self):
        print('w')
        for (state, choice) in self.moves_played:
            #self.known_states[state].append([choice, choice, choice])
            self.known_states[state].append(choice)
        self.wins += 1

    def draw_game(self):
        print('d')
        self.draws += 1
    
    def lose_game(self):
        print('l')
        for (state, choice) in self.moves_played:
            del self.known_states[state][self.known_states[state].index(choice)]
        self.losses += 1

class Random:
    def __init__(self, mark):
        self.mark = mark
    
    def start_game(self):
        pass

    def get_move(self, state, moves):
        move = random.choice(moves)
        return move
    
    def end_game(self, winner):
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
        if (winner == self):
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
        
        return bestScore

    else:
        bestScore = 2
        for move in moves:
            state.play_move(move, state.get_player().mark)
            score = minimax(state, state.get_moves(), True, depth+1)
            state.play_move(move, ' ')
            if (score < bestScore):
                bestScore = score
                  
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
        winner = state.check_winner()
        if (winner or len(moves) - 1 < 1):
            player1.end_game(winner)
            player2.end_game(winner)
            return

if __name__ == '__main__':
    player1 = Random('X')
    player2 = Menace('O')
    count = 0
    while count < 500:
        play_game(player1, player2)
        play_game(player2, player1)
        count += 1
    player1 = Player('X')
    while True:
        print("\n\nStarting new game: ")
        play_game(player1, player2)
        print("\n\nStarting new game: ")
        play_game(player2, player1)