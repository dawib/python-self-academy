from random import randrange, randint, shuffle, sample
from os import system
from time import sleep

class Sudoku:
#class for managing sudoku game
    def __init__(self,board=[['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.']]):
        self.board = board.copy()
        #the sudoku is empty by default

    def print(self):
        #esthetic printing function
        for i in range(3):
            for j in range(3):
                line = ''
                for k in range(3):
                    for l in range(3):
                        line+=self.board[3*i+j][3*k+l]
                        line+=' '
                    if k<2:
                        line+='| '
                
                print(line)
            
            if i<2:
                print("- - - + - - - + - - -")
    
    def basic_print(self):
        #trivial printing function
        for i in range(9):
            line=''
            for j in range(9):
                line+=str(self.board[i][j])
                line+=' '
            print(line)
                
    def input(self):
        #function for writing sudoku manually
        for i in range(9):
            print("Write",i+1,"\b-th row:")
            line = input()
            self.board[i] = list(line)
            
   
    def erase(self):
        #empty the board completely
        self.board = [['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.','.','.']]
                      
    def make_move(self,x,y,d):
        self.board[x][y]=str(d)
        
    def erase_move(self,x,y):
        self.board[x][y]='.'
        
    def is_ok(self):
    #checking if the sudoku is correct
        #rows
        for i in range(9):
            used = [0,0,0,0,0,0,0,0,0]
            for j in range(9):
                if self.board[i][j]!='.':
                    if used[int(self.board[i][j])-1]>0:
                        return False
                    else:
                        used[int(self.board[i][j])-1]+=1
        
        #columns
        for j in range(9):
            used = [0,0,0,0,0,0,0,0,0]
            for i in range(9):
                if self.board[i][j]!='.':
                    if used[int(self.board[i][j])-1]>0:
                        return False
                    else:
                        used[int(self.board[i][j])-1]+=1
                        
        #blocks
        for i in range(3):
            for j in range(3):
                used = [0,0,0,0,0,0,0,0,0]
                for k in range(3):
                    for l in range(3):
                        if self.board[3*i+k][3*j+l]!='.':
                            if used[int(self.board[3*i+k][3*j+l])-1]>0:
                                return False
                            else:
                                used[int(self.board[3*i+k][3*j+l])-1]+=1
                                
        #if the function reached this moment then everything is ok
        return True 
        
    def is_full(self):
    #checking if the board is full
        for i in range(9):
            for j in range(9):
                if self.board[i][j]=='.':
                    return False
                    
        return True
        
#    def solve(self,x=-1,y=-1):
#        #system('clear')
#        #self.print()
#        #sleep(.05)
##        #if sudoku is not correct, erase the last move and return that it is not solved 
#        if not self.is_ok():
#            return False
#        
#        #if the board is full, don't do anything and return that the sudoku is solved
#        if self.is_full():
#            return True
#       
#        #if the board is not full 
#        #find the first free place
#        br=0
#        for i in range(9):
#            for j in range(9):
#                if self.board[i][j]=='.':
#                    a,b=i,j
#                    br=1
#                    break
#            if br==1:
#                break 
#       
#        #try putting consecutive numbers in the free place
#        for d in range(9):
#            self.make_move(a,b,d+1)
#            success = self.solve(a,b)
#            if success:
#                return True 
#            else:
#                self.erase_move(a,b)
#                
#        return False 
    
    def count_solutions(self,x=-1,y=-1,num_sol=0,printing=False):
    #count the number of all solutions
        #if sudoku is not correct, return that it is not solved - do not count this branch
        if not self.is_ok():
            return num_sol 
        
        #if the board is full, don't do anything and return that the sudoku is solved - increase the counter
        if self.is_full():
            if printing:
                self.print()
                print('======================')
            return num_sol+1
       
        #if the board is not full 
        #find the first free place
        for i in range(81):
            if self.board[i//9][i%9]=='.':
                a,b=i//9,i%9
                break
       
        #try putting consecutive numbers in the free place and count the subsequent solutions
        for d in range(9):
            self.make_move(a,b,d+1)
            pr=printing
            n=num_sol
            num_sol = self.count_solutions(x=a,y=b,num_sol=n,printing=pr)
            self.erase_move(a,b)
                
        return num_sol 
        
    def has_more_than_one_solution(self,x=-1,y=-1,num_sol=0):
    #check if the sudoku has more than one solution
        #if the counter is above 1, return it
        if num_sol>1:
            return num_sol
    
        #if sudoku is not correct, return the current state of the counter
        if not self.is_ok():
            return num_sol 
        
        #if the board is full, increase the counter
        if self.is_full():
            return num_sol+1
       
        #if the board is not full 
        #find the first free place
        for i in range(81):
            if self.board[i//9][i%9]=='.':
                a,b=i//9,i%9
                break
       
        #try putting consecutive numbers in the free place
        for d in range(9):
            self.make_move(a,b,d+1)
            n=num_sol
            num_sol = self.has_more_than_one_solution(x=a,y=b,num_sol=n)
            self.erase_move(a,b)
            if num_sol>1:
                return num_sol
            
                
        return num_sol 
        
    def solve(self,x=-1,y=-1,rnd=False):
        #if sudoku is not correct, return that it is not solved 
        if not self.is_ok():
            return False
        
        #if the board is full, don't do anything and return that the sudoku is solved
        if self.is_full():
            return True
       
        #if the board is not full 
        #find the first free place
        order = list(range(81))
        if rnd:
            shuffle(order)
        
        for i in range(81):
            if self.board[i//9][i%9]=='.':
                a,b = i//9,i%9 
                break 
       
        #try putting numbers in a random order in the free place
        nums = [1,2,3,4,5,6,7,8,9]
        if rnd:
            shuffle(nums)
        for d in nums:
            self.make_move(a,b,d)
            success = self.solve(a,b,rnd)
            if success:
                return True 
            else:
                self.erase_move(a,b)
                
        return False 
    
    def generate(self,dir='down'):
        if dir=='down':
            self.erase()
            #fill in randomly
            self.solve(rnd=True)
        
            order = list(range(81))
            shuffle(order)
        
            for i in order: 
                d = self.board[i//9][i%9]
                self.erase_move(i//9,i%9)
                s = self.count_solutions()
                if s>1:
                    self.make_move(i//9,i%9,d)
           
        else:
            self.erase()
            order = list(range(81))
            shuffle(order)
            
            for i in order:
                nums = list(range(9))
                shuffle(nums)
                for d in nums:
                    self.make_move(i//9,i%9,d+1)
                    s = self.has_more_than_one_solution()
                    if s==0:
                        self.erase_move(i//9,i%9)
                    else:
                        break
                
                if s==1:
                    break 