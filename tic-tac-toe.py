import random

class TicTacToe: 

    def __init__(self):
        self.game = [(['-'] * 3) for i in range (3)]
        self.moves = [[i + 1 + 3 * j for i in range(3)] for j in range(3)]
        self.move_count = 0
        self.status = 0
        # 0 = x to play, 1 = y to play, 2 = draw, 3 = x won, 4 = o won

    def print_grid(self, grid): 
        print()
        for row in grid: 
            for i in range (len(row)):
                if i != 0:
                    print("|", end="") 
                print(" " + str(row[i]), end=" ")
            print()
        print()


    def is_game_over(self): 
        # checking diagonal wins
        if (self.game[0][0] == self.game[1][1] == self.game[2][2] or self.game[0][2] == self.game[1][1] == self.game[2][0]) and self.game[1][1] != '-':
            print(self.game[1][1], "won!")
            return True
        # checking row or column wins 
        for i in range(3): 
            if self.game[i][1] != '-' and self.game[i][0] == self.game[i][1] == self.game[i][2]:
                print(self.game[i][1], "won!")
                self.status += 3 
                return True
            elif self.game[1][i] != '-' and self.game[0][i] == self.game[1][i] == self.game[2][i]:
                print(self.game[1][i], "won!")
                self.status += 3 
                return True
            
        if self.move_count == 9: 
            self.status = 2 
            print("draw!")
            return True

    def make_move(self, move, player):
        column = (move - 1) % 3
        row = (move - 1) // 3
        if self.moves[row][column] == '*':
            return False
        self.game[row][column] = player
        self.moves[row][column] = '*'
        return True
    
    def player_move(self, player='x'):
        self.print_grid(self.game)
        self.print_grid(self.moves)
        print(player + "'s move")
        move = input("enter your move: ")
        
        try: 
            move = int(move)
        except: 
            if move == "quit":
                exit()
            print("that's not a move!")
            return self.player_move(player)

        if not self.make_move(move, player): 
            print("cannot make a move there!")
            return self.player_move(player)
    
    def agent_move(self, agent='o'): 
        move = random.randint(0,9)
        if not self.make_move(move, agent):
            return self.agent_move(agent)

    def play_game(self, opponent_move, player='x'):
        opponent = 'o' if player == 'x' else 'x'
         
        while self.status < 2: 
            if self.status == 0:
                self.player_move(player)
            else: 
                opponent_move(opponent)
            self.status = (self.status + 1) % 2
            
            self.move_count += 1 
            if self.is_game_over():
                self.print_grid(self.game)
                break 

        print('thank you for playing!')

def start_game(): 
    tictactoe = TicTacToe()
    print("welcome to tic-tac-toe!\n    who do you wanna play with?\n\t1. random agent\n\t2. against a friend")
    choice = input("enter your choice (type 'quit' to exit at any point): ")
    if choice in "1. random agent":
        tictactoe.play_game(tictactoe.agent_move)
    elif choice == "quit": 
        exit()
    else: 
        tictactoe.play_game(tictactoe.player_move)


if __name__ == "__main__": 
    start_game()
    

    
