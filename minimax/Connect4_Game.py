import Connect4_Ai
import math
import numpy as np
import matplotlib.pyplot as plt


# CONSTANTS
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

ROW_COUNT = 6
COLUMN_COUNT = 7

WINDOW_LENGTH = 4

heuristic3 = Connect4_Ai.score_position
heuristic2 = Connect4_Ai.evaluate_board1
heuristic1 = Connect4_Ai.evaluate_board2

class Grid:
    def __init__(self):
        self.num = 1
        self.players = {
            1 : [2, heuristic2], #depth, heuristic
            2 : [2, heuristic1]
        }
        self.grid = [[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]]
        self.gameOver = False
        self.winner = ""
        self.draw = False

    def Drop(self, column):
        i = 0
        for i in range(6):
           if self.grid[column][i] != 0:
                self.grid[column][i-1] = self.num
                break
           elif i == 5:
                self.grid[column][i] = self.num
                
    def CheckDiagonal(self, row, column, inrow, left):#left = -1, right = 1, up 1, down -1
        column += left
        row -= 1

        if column < 7 and row < 6:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckDiagonal(row, column, inrow, left)


    def CheckVertical(self, row, column, inrow):
        row -= 1
        if row != -1:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckVertical(row, column, inrow)


    def CheckHorizontal(self, row, column, inrow):
        column += 1
        if column != 7:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckHorizontal(row, column, inrow)


    #def PieceWinCheck(self):
    #    for i in range(7):
     #       for u in range (6):
      #          if self.grid[i][u] == self.num:
       #             self.CheckDiagonal(u, i, 1, -1)
        #            self.CheckDiagonal(u, i, 1, 1)
         #           self.CheckHorizontal(u, i, 1)
          #          self.CheckVertical(u, i, 1)

    
    def SwapTurn(self):
        if self.num == 1:
            self.num = 2
        else:
            self.num = 1

    def Display(self):
        grid = self.grid
        print(grid[0][0], grid[1][0], grid[2][0], grid[3][0], grid[4][0], grid[5][0], grid[6][0])
        print(grid[0][1], grid[1][1], grid[2][1], grid[3][1], grid[4][1], grid[5][1], grid[6][1])
        print(grid[0][2], grid[1][2], grid[2][2], grid[3][2], grid[4][2], grid[5][2], grid[6][2])
        print(grid[0][3], grid[1][3], grid[2][3], grid[3][3], grid[4][3], grid[5][3], grid[6][3])
        print(grid[0][4], grid[1][4], grid[2][4], grid[3][4], grid[4][4], grid[5][4], grid[6][4])
        print(grid[0][5], grid[1][5], grid[2][5], grid[3][5], grid[4][5], grid[5][5], grid[6][5])

    def Turn(self, column):
        self.Drop(column)
        # self.Display()
        self.gameOver = Connect4_Ai.PieceWinCheck(self.grid, self.num)
        if self.gameOver == True:
            readableWinner = ""
            if self.num == 1:
                readableWinner = "H1"
            elif self.num == 2:
                readableWinner = "H2"

            self.winner = readableWinner
            print("##############################")
            print("The ", readableWinner, " has won")
            print("##############################")
            self.Display()
            
        #else:
            #self.SwapTurn() #removed to change how turns are handled
            #self.Turn() #removed to change how turns are handled

    def Gameplay(self, first_player):
        print("FIRST PLAYER IS: "+str(first_player))
        runTime = 0
        # depth = 6
        roundsPlayed = 0

        while self.gameOver == False:
            #player 1 turn (Human)
            
            self.num = first_player
            print("First Player's Turn: Player with Strategy " + str(self.players[self.num][1]) + " and depth " + str(self.players[self.num][0]))
            
            #Ai suggestion for human
            minimax_h1 = Connect4_Ai.minimax(self.grid, self.players[self.num][0], -math.inf, math.inf, True, self.players[self.num][1])
            aiColumnIndex = minimax_h1[0]

            #validate human inputs
            # column = int(input("select a column 1-7: "))
            # while self.ValidatePlayerTurn(column) == False:
            #     column = int(input("select a column 1-7: "))
            # columnIndex = column - 1

            #bullying the human
            # print("") #line break
            # if aiColumnIndex == columnIndex:
            #     print("CONGRATULATIONS you played the best move for this scenario")
            # else:
            #     print("That was not the best move")
            #     print("You should have played column "+str(aiColumnIndex+1))
            # print("") #line break

            if aiColumnIndex == None and minimax_h1[1] == 0:
                self.gameOver = True
                self.draw = True
                print("The game is a draw")
            else:
                self.Turn(aiColumnIndex)

            #player 2's turn (AI)
            if self.gameOver == False:
                
                print("")
                
                # print("Ai is thinking with a depth of "+str(depth))
                self.num = 3 - first_player 
                print(self.num)
                print("Second Player's Turn: Player with strategy " + str(self.players[self.num][1]) + " and depth " + str(self.players[self.num][0]))
                #AI Decision with timer
          
                minimax_h2 = Connect4_Ai.minimax(self.grid, self.players[self.num][0],-math.inf, math.inf, True, self.players[self.num][1])[0]
                column = minimax_h2
                #output a few stats 
                # print("MinMax Algorithm took "+str(runTime)+"s to run at a depth of "+str(depth))
                #print("Ratio of Ai wins/Player Wins "+str(aiWinNum)+"/"+str(p1WinNum))
                #print("Ratio: "+str(aiWinNum/p1WinNum))
                print("")
                #tune depth to in
                # crease accuracy as runtime decreases
                # if runTime < approxRunTime - 2.5 and roundsPlayed > 4:
                #     depth += 1
                #     print("Depth increased to "+str(depth))
                # elif runTime > approxRunTime + 2.5 and runTime > 6 and roundsPlayed > 4:
                #     depth -= 1
                #     print("Depth decreased to "+str(depth))
                if column == None and minimax_h1[1] == 0:
                    self.gameOver = True
                    self.draw = True
                    print("The game is a draw")
                else:
                    self.Turn(column)  
                print("")
                print("The AI has played column "+str(column+1))
                print("")

    def GetWinRate(self, games, epochs):
        win_percentages_h1 = []
        win_percentages_h2 = []
        drawss = []
        
        for _ in range(epochs):
            print("##############################")
            print("Epoch "+str(_+1))
            print("##############################")
            h2Win = 0
            h1Win = 0
            draws = 0
            for i in range(games):
                print("Game "+str(i+1))
                self.gameOver = False
                self.grid = [[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]]
                self.winner = ""
                self.draw = False
                self.players = {
                1 : [5, heuristic2], #depth, heuristic
                2 : [5, heuristic3]
            }
                if i % 2 == 0:
                    starting_player = 2
                else:
                    starting_player = 1
                self.num = starting_player

                self.Gameplay(starting_player)

                if self.winner == "H2": 
                    h2Win += 1
                elif self.winner == "H1": 
                    h1Win += 1
                elif self.draw:
                    draws += 1
                else:
                    print("Error in GetWinRate")
            
            player1_win_percentage = (h1Win/games) * 100
            player2_win_percentage = (h2Win/games) * 100
            draw_percentage = (draws/games) * 100

            print("##############################")
            print("The Heuristic of player 1 won "+str(h1Win)+" times")
            print("The Heuritic of player 2 won "+str(h2Win)+" times")
            print("Draws "+str(draws)+" times")

            # Labels for the bars
            labels = ['Heuristic 2 Wins', 'Heuristic 3 Wins', 'Draws']

            # Heights of the bars
            heights = [player1_win_percentage, player2_win_percentage, draw_percentage]

            # Colors for the bars
            colors = ['red', 'green', 'grey']

            # Plotting the bars
            plt.bar(labels, heights, color=colors)

            # Adding labels and title
            plt.xlabel('Outcomes')
            plt.ylabel('Percentage')
            plt.ylim(0, 100)
            plt.title('Comparison of Outcomes')

            # Displaying the plot
            plt.show()

        # print("##############################")
        # print("Heuristic 1 win rates: "+str(win_percentages_h1))
        # print("Heuristic 2 win rates: "+str(win_percentages_h2))
        # print("Draws: "+str(drawss))
        # # plt.plot(win_percentages_h1, label = "Heuristic 1")
        # plt.figure(figsize=(10, 5))
        # plt.subplot(1, 2, 1)
        # plt.plot(range(1, epochs + 1), win_percentages_h1, marker="o")
        # # plt.plot(range(1, epochs + 1), win_percentages_h2, marker="x")
        # # plt.plot(range(1, epochs + 1), draws, linestyle="--", color="gray")
        # plt.title("Win Rate Over Epochs")
        # plt.xlabel("Epochs")
        # plt.ylabel("Win Rate (%)")
        # plt.grid(True)
        # plt.show()
    
    def ValidatePlayerTurn(self,column):
        columnIndex = column - 1
        #checks for blank input
        if column == None:
            print("please input a number: ")
            return False
        
        #checks for vaild column number
        column = int(column)
        if column < 1 or column > 7:
            print("number must be between 1-7")
            return False

        #checks column isnt full
        grid = self.grid

        if grid[columnIndex][0] == 0:
            return True
        else:
            print("The selected row is full")
            return False
  
game = Grid()
game.Display()
# game.Gameplay(10) #lower numbers are easier, higher numbers are harder
game.GetWinRate(10, 1)