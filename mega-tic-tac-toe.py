moves_grid = ''' 
           |#|           |#|          
     1     |#|     2     |#|     3     
           |#|           |#|          
#######################################
           |#|           |#|          
     4     |#|     5     |#|     6     
           |#|           |#|          
#######################################
           |#|           |#|          
     7     |#|     8     |#|     9     
           |#|           |#|          
'''
class MegaTicTacToe:
    def __init__(self):
        self.game = [[(['-'] * 3) for i in range (3)] for j in range (9)]
        self.moves = [[[i + 1 + 3 * j for i in range(3)] for j in range(3)]for k in range(9)]
        self.move_count = [0] * 9
        self.current_game = 0
        self.status = 0
        self.mega_grid = [(['-'] * 3) for i in range (3)]


    def print_game(self, move=False): 
        print()
        rows = [''] * 3
        # for each of the 9 games
        for i in range(9): 
            # for each of the 3 rows
            for j in range(3):
                if (i % 3) != 0: 
                    rows[j] += " |#|"

                for k in range(3):   
                    if not move: 
                        if k != 0: 
                            rows[j] += " |" 
                        rows[j] += " "  + str(self.game[i][j][k])
                    else: 

                        if k != 0: 
                            rows[j] += "  " if i + 1 != self.current_game else " |"
                        if(i + 1 == self.current_game): 
                            rows[j] += " "  + str(self.moves[i][j][k])
                        else: 
                            rows[j] += "  " 
            if (i + 1) % 3 == 0: 
                if (i != 2): 
                    print('#' * 39)
                for row in rows: 
                    print(row)
                rows = [''] * 3
        print()

    def player_move(self, player='x'):
        self.print_game()
        self.print_game(True)
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
        return move
        
    def make_move(self, move, player):
        column = (move - 1) % 3
        row = (move - 1) // 3
        if self.moves[self.current_game - 1][row][column] == '*':
            return False
        self.game[self.current_game - 1][row][column] = player
        self.moves[self.current_game - 1][row][column] = '*'
        return True

    def play_game(self, player='x'):
        while self.status < 2: 
            if (self.current_game == 0):
                print(moves_grid)
                try: 
                    current_game = int(input("select your game to play in : "))
                    column = (current_game - 1) % 3
                    row = (current_game - 1) // 3
                    if self.mega_grid[row][column] == '-':
                        self.current_game = current_game
                    else: 
                        print("can't play there!")
                        self.play_game()    
                except: 
                    print("that is not a move!")
                    self.play_game()
            else: 
                opponent = 'o' if player == 'x' else 'x'

                if self.status == 0:
                    move = self.player_move(player)
                else: 
                    move = self.player_move(opponent)
                self.status = (self.status + 1) % 2
                
                self.move_count[self.current_game - 1] += 1 
                column = (self.current_game - 1) % 3
                row = (self.current_game - 1) // 3
                if self.is_game_over(self.game[self.current_game - 1]):
                    self.mega_grid[row][column] = player
                    self.game[self.current_game - 1] = [[player if i == 1 and j == 1 else ' ' for i in range(3)] for j in range(3)]
                column = (move - 1) % 3
                row = (move - 1) // 3
                self.current_game = move if self.mega_grid[row][column] == '-' else 0

                if self.is_game_over(self.mega_grid):
                    self.print_grid(self.game)
                    break 


    def is_game_over(self, game): 
        # checking diagonal wins
        if (game[0][0] == game[1][1] == game[2][2] or game[0][2] == game[1][1] == game[2][0]) and game[1][1] in 'xo':
            # print(game[1][1], "won!")
            return True
        # checking row or column wins 
        for i in range(3): 
            if game[i][1] != '-' and game[i][0] == game[i][1] == game[i][2]:
                # print(game[i][1], "won!")
                # self.status += 3 
                return True
            elif game[1][i] != '-' and game[0][i] == game[1][i] == game[2][i]:
                # print(game[1][i], "won!")
                # self.status += 3 
                return True
    



    def start_game(self): 
        print("welcome to mega tic-tac-toe")
        print("rules\n\t1. first player can play in any of the 9 games. their opponent has to play in the game corresponding to the square they played in.")
        print("\t2. if a player wins one of the small games, the whole thing is marked as their symbol (x or o). the objective of is to win the big game")
        print("\t3. if the corresponding game to the move of one's opponent has been won or drawn, the player can choose to play in whichever game they like.")
        while True:
            self.play_game()
        # self.print_game(True)
        

        
        


if __name__ == "__main__": 
    megatictactoe = MegaTicTacToe()
    megatictactoe.start_game()

    

    
