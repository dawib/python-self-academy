from random import randrange

class Board:
#class for managing board of a tic-tac-toe game
    def __init__(self):
        self.board = [['.','.','.'],['.','.','.'],['.','.','.']]
        
    def this_move_is_valid(self,x,y):
    #check if the move at the given position is allowed
        return self.board[x][y]=='.'
        
    def print(self):
        for i in range(3):
            print(self.board[i][0],self.board[i][1],self.board[i][2])
       
    def winner(self):
    #check if someone has won the game and return the winner
        #rows and columns
        for i in range(3):
            if self.board[i][i]!='.':
                if self.board[i][0]==self.board[i][1] and self.board[i][1]==self.board[i][2]:
                    return self.board[i][i]
                if self.board[0][i]==self.board[1][i] and self.board[1][i]==self.board[2][i]:
                    return self.board[i][i]
                    
        #diagonals
        if self.board[1][1]!='.':
            if self.board[0][0]==self.board[1][1] and self.board[1][1]==self.board[2][2]:
                return self.board[1][1]
            if self.board[0][2]==self.board[1][1] and self.board[1][1]==self.board[2][0]:
                return self.board[1][1]
                
        #if nobody has won return N
        return 'N'
        
    def is_full(self):
    #check if the board is full
        for i in range(3):
            for j in range(3):
                if self.board[i][j]=='.':
                    return False
                    
        return True
       
    def make_move(self,x,y,mark):
    #put a mark in the given position
        self.board[x][y]=mark
        
    def erase(self,x,y):
        self.board[x][y]='.'
        
    def randomize(self):
    #fill the board randomly
        for i in range(3):
            for j in range(3):
                r = randrange(3)
                if r==0:
                    self.make_move(i,j,'O')
                elif r==1:
                    self.make_move(i,j,'X')
                else:
                    self.make_move(i,j,'.')
     
    def evaluate(self,depth,isMax):
    #evaluate the score of the board - O wants to minimize it, X wants to maximize
        W = self.winner()
        
        if W=='O':
            return -100+depth
        elif W=='X':
            return 100-depth
            
        if self.is_full():
            return 0
            
        if isMax:
        #the evaluating player is X
            val = -101
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]=='.':
                        self.make_move(i,j,'X')
                        v = self.evaluate(depth+1,not isMax)
                        self.erase(i,j)
                        if v>val:
                            val=v
            
            return val
            
        elif not isMax:
        #the evaluating player is O 
            val = 101
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]=='.':
                        self.make_move(i,j,'O')
                        v = self.evaluate(depth+1,not isMax)
                        self.erase(i,j)
                        if v<val:
                            val=v 
                        
            return val
            
    def optimal_move(self,mark):
        if mark=='O':
            val = 101
            x,y = 3,3
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]=='.':
                        self.make_move(i,j,mark)
                        v=self.evaluate(0, True)
                        self.erase(i,j)
                        if v<val:
                            val=v
                            x,y=i,j 
                            
            return x,y 
            
        else:
            val = -101
            x,y = 3,3
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]=='.':
                        self.make_move(i,j,mark)
                        v=self.evaluate(0, False)
                        self.erase(i,j)
                        if v>val:
                            val=v
                            x,y=i,j 
                            
            return x,y 
            
    def make_optimal_move(self,mark):
        x,y = self.optimal_move(mark)
        self.make_move(x,y,mark)
        
    

