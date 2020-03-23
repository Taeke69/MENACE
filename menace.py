#import numpy as np
import random
#from time import sleep

class State:
    # Het spel wordt aangemaakt
    def __init__(self, player1, player2):
        # De toestand van het spel wordt aangemaakt
        self.state = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        # De spelers worden toegevoegd aan het spel
        self.player1 = player1
        self.player2 = player2
        # De verschillende rotaties van het spel worden geïnitialiseerd
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

    # Verkrijgen van de toestand om weer te geven
    def get_state(self):
        return("\n 0 | 1 | 2 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 3 | 4 | 5 \t  %s | %s | %s \n"
                "---+---+--- \t ---+---+---\n"
                " 6 | 7 | 8 \t  %s | %s | %s \n" % 
                (self.state[0], self.state[1], self.state[2],
                self.state[3], self.state[4], self.state[5],
                self.state[6], self.state[7], self.state[8]))

    # Verkrijgen van de toestand als string
    def get_string(self):
        return str(self.state)

    # Verkrijgen van de zetten voor de huidige toestand
    def get_moves(self):
        moves = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                moves.append(i)
        return moves

    # Spelen van een zet in het spel
    def play_move(self, move, mark):
        self.state[move] = mark

    # Controleren of de zet die wordt gekozen valide is
    def validate_move(self, move):
        try:
            move = int(move)
        except ValueError:
            return False
        if 0 <= move < 9 and self.state[move] == ' ':
            return True
        else:
            return False

    # Verkrijgen van de speler die aan de beurt is
    def get_player(self):
        count_x = 0
        count_o = 0
        for mark in self.state:
            if mark == self.player1.mark:
                count_x += 1
            if mark == self.player2.mark:
                count_o += 1
        return (self.player2 if count_x > count_o else self.player1)

    # Verkrijgen van de verschillende rotaties van de toestand
    def get_rotations(self):
        state_rotations = []
        for rotation in self.rotations:
            x = []
            for i in rotation:
                x.append(self.state[i])
            state_rotations.append(str(x))
        return state_rotations

    # Het terugzetten van een zet naar de originele toestand
    def unrotate_move(self, rotation, move):
        return self.rotations[rotation][move]

    # Controleren of er een winnaar is
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
    # Aanmaken van Menace
    def __init__(self, mark):
        # Menace krijgt 'X' of 'O' toegewezen
        self.mark = mark
        # Initialiseren van een variabele voor de bekende toestanden
        self.known_states = {}
        # Initialiseren van variabeles voor uitkomsten van het spel
        self.wins = 0
        self.draws = 0
        self.losses = 0
        
    # Starten van het spel
    def start_game(self):
        # Initialiseren van een variabele voor de zetten die worden gespeeld
        self.moves_played = []

    # Verkrijgen van een zet
    def get_move(self, state, moves):
        # Opslaan van toestand als string
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
        # Rotaties worden opgehaald
        rotations = state.get_rotations()
        # Controleren of één van de rotaties al aanwezig is in de bekende toestanden
        known_rotations = [rotation in self.known_states for rotation in rotations]

        # Initialiseren van een variabele voor de rotatie
        rotation_index = -1

        # Controleren welke rotatie is opgeslagen in de variabele
        for i in range(len(known_rotations)):
            if known_rotations[i]:
                rotation_index = i

        # Als er geen variabele is opgeslagen -> Toevoegen van toestand aan de variabele
        if rotation_index == -1:
            # Huidige rotatie = standaard rotatie = 0
            rotation_index = 0
            # Kopiëren van toestand
            state_c = state
            # Initialiseren van variabele voor beste score en beste zet
            bestScore = -2
            bestMove = []
            for x in moves:
                print(x)
                # Spelen van zet op dummy toestand
                state_c.play_move(x, self.mark)
                # Ophalen van score uit het minimax algoritme
                score = minimax(state_c, state_c.get_moves(), False, 0)
                # Terugzetten van toestand naar toestand voor de zet
                state_c.play_move(x, ' ')
                # Bij gelijke score -> zet toevoegen aan variabele
                if (score == bestScore):
                    bestMove.append(x)
                # Bij betere score -> zetten verwijderen -> score opslaan en zet toevoegen aan variabele
                elif (score > bestScore):
                    del bestMove[:]
                    bestScore = score
                    bestMove.append(x)
                    print('score', score)
                    print('x', x)
            
            # De beste zetten met de toestand opslaan in variabele
            self.known_states[state_s] = bestMove
            print('new situation', self.known_states[state_s])

        # Opslaan van staat voor bekende rotatie
        state_r = rotations[rotation_index]
        print('known_state', self.known_states[state_r])
        # Opslaan van zetten voor bekende rotatie
        choices = self.known_states[state_r]
        print('choices', choices)
        # Als er zetten aanwezig zijn -> Kiezen van willekeurige zet
        if len(choices):
            choice = random.choice(choices)
        # Geen zetten aanwezig -> Verwijder toestand en doe functie nog een keeer
        else:
            del self.known_states[state_r]
            choice = self.get_move(state, state.get_moves())
        # Toeveogen van zet aan variabele
        self.moves_played.append((state_r, choice))
        # Terugzetten van de zet naar originele toestand
        choice = state.unrotate_move(rotation_index, choice)

        return choice

    # Uitvoeren van acties aan het einde van het spel
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

    # Toevoegen van zet aan variabele bij winst
    def win_game(self):
        print('w')
        for (state, choice) in self.moves_played:
            self.known_states[state].append(choice)
        self.wins += 1

    # Geen actie ondernemen bij gelijkspel
    def draw_game(self):
        print('d')
        self.draws += 1
    
    # Verwijderen van zet uit variabele bij verlies
    def lose_game(self):
        print('l')
        for (state, choice) in self.moves_played:
            del self.known_states[state][self.known_states[state].index(choice)]
        self.losses += 1

class Human:
    # Menselijke speler wordt aangemaakt
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

# Minimax algoritme voor het achterhalen van de beste zet
def minimax(state, moves, isMaxPlayer, depth):
    # Controleren of er een winnaar is:
    # Is er een winnaar en MaxPlayer is aan de beurt -> MaxPlayer verliest -> -1
    # Is er een winnaar en Maxplayer is niet aan de beurt -> MaxPlayer wint -> 1
    # Is er geen winnaar en zijn er geen zetten mogelijk -> Gelijkspel -> 0
    winner = state.check_winner()
    if (winner):
        if isMaxPlayer:
            return -1
        elif not isMaxPlayer:
            return 1
    if (len(moves) < 1 or depth == 10):
        return 0

    # Als MaxPlayer aan de beurt is -> hoogste score teruggeven
    if isMaxPlayer:
        bestScore = -2
        for move in moves:
            state.play_move(move, state.get_player().mark)
            score = minimax(state, state.get_moves(), False, depth+1)
            state.play_move(move, ' ')
            if (score > bestScore):
                bestScore = score
        
        return bestScore
    # Als MaxPlayer niet aan de beurt is -> laagste score teruggeven
    else:
        bestScore = 2
        for move in moves:
            state.play_move(move, state.get_player().mark)
            score = minimax(state, state.get_moves(), True, depth+1)
            state.play_move(move, ' ')
            if (score < bestScore):
                bestScore = score
                  
        return bestScore

# Starten van het spel
def play_game(player1, player2):
    # Spel aanmaken en spel starten voor spelers
    state = State(player1, player2)
    player1.start_game()
    player2.start_game()
    # Verloop van het spel in een while loop
    while True:
        print(state.get_state())
        current_player = state.get_player()
        moves = state.get_moves()
        move = current_player.get_move(state, moves)
        state.play_move(move, current_player.mark)
        winner = state.check_winner()
        # Als er een winnaar is of geen zetten meer mogelijk zijn -> spel beëindigen
        if (winner or len(moves) - 1 < 1):
            player1.end_game(winner)
            player2.end_game(winner)
            return

# Main functie
if __name__ == '__main__':
    # Aanmaken van spelers
    player1 = Human('X')
    player2 = Menace('O')
    # Starten van spel met spelers (om de beurt beginnen)
    while True:
        print("\n\nStarting new game: ")
        play_game(player1, player2)
        print("\n\nStarting new game: ")
        play_game(player2, player1)