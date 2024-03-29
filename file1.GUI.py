import random
import pygame
import math
import time 
from copy import deepcopy
class BoxesandGridsGame():
    def __init__(self):
        pass
        #1
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        #2
        self.hColor=[[0 for x in range(6)] for y in range(7)]
        self.vColor=[[0 for x in range(7)] for y in range(6)]
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        self.boardh_temp = self.boardh
        self.boardv_temp = self.boardv
        self.initGraphics();
        self.drawBoard();
        self.hColor=[[0 for x in range(6)] for y in range(7)]
        self.vColor=[[0 for x in range(7)] for y in range(6)]
        
        self.goal_x=6;
        self.goal_y=5;
        self.initial_move=[0,0,0];
        
        
        self.score_player1=0;
        self.score_player2=0;
        
    def update(self):
    #sleep to make the game 60 fps
        self.clock.tick(60)

    #clear the screen
        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()

        for event in pygame.event.get():
        #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
        print ('before making a move')
        self.player2();
        print ('move made by player 2')
        self.player1();
        print ('move made by player 1')
    #update the screen
    
        pygame.display.flip()
    def initGraphics(self):
        self.normallinev=pygame.image.load("normalline.png")
        self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.bar_donev=pygame.image.load("bar_done.png")
        self.bar_doneh=pygame.transform.rotate(pygame.image.load("bar_done.png"), -90)
        self.bar_donev_r=pygame.image.load("bar_done_red.png")
        self.bar_doneh_r=pygame.transform.rotate(pygame.image.load("bar_done_red.png"), -90)
        self.bar_donev_g=pygame.image.load("bar_done_green.png")
        self.bar_doneh_g=pygame.transform.rotate(pygame.image.load("bar_done_green.png"), -90)
        self.bar_donev_r_l=pygame.image.load("bar_done_light_red.png")
        self.bar_doneh_r_l=pygame.transform.rotate(pygame.image.load("bar_done_light_red.png"), -90)
        self.bar_donev_g_l=pygame.image.load("bar_done_light_green.png")
        self.bar_doneh_g_l=pygame.transform.rotate(pygame.image.load("bar_done_light_green.png"), -90)
        self.hoverlinev=pygame.image.load("hoverline.png")
        self.hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
        self.separators=pygame.image.load("separators.png")
        self.redindicator=pygame.image.load("redindicator.png")
        self.greenindicator=pygame.image.load("greenindicator.png")
        self.greenplayer=pygame.image.load("greenplayer.png")
        self.blueplayer=pygame.image.load("blueplayer.png")
        self.winningscreen=pygame.image.load("youwin.png")
        self.gameover=pygame.image.load("gameover.png")
        self.score_panel=pygame.image.load("score_panel.png")
    def drawBoard(self):
        for x in range(6):
            for y in range(7):
                
                if  (self.hColor[y][x]==-1):
                    self.screen.blit(self.bar_doneh_r, [(x)*64+5, (y)*64])
                elif  self.hColor[y][x]==1:
                    self.screen.blit(self.bar_doneh_g, [(x)*64+5, (y)*64])
                else:
                    self.screen.blit(self.bar_doneh, [(x)*64+5, (y)*64])
                    
        for x in range(7):
            for y in range(6):
                
                if  (self.vColor[y][x]==-1):
                    self.screen.blit(self.bar_donev_r, [(x)*64, (y)*64+5])
                elif  self.vColor[y][x]==1:
                    self.screen.blit(self.bar_donev_g, [(x)*64, (y)*64+5])
                else:
                    self.screen.blit(self.bar_donev, [(x)*64, (y)*64+5])
          
                  
        for x in range(7):
            for y in range(7):
                self.screen.blit(self.separators, [x*64, y*64])
                
    def drawHUD(self):
    #draw the background for the bottom:
        self.screen.blit(self.score_panel, [0, 389])
        #create font
        myfont = pygame.font.SysFont(None, 32)

        #create text surface
        label = myfont.render("Player 1:", 1, (255,255,255))

        #draw surface
        self.screen.blit(label, (10, 400))
        #same thing here
        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.score_player1), 1, (255,255,255))
        scoreother = myfont64.render(str(self.score_player2), 1, (255,255,255))
        scoretextme = myfont20.render("Player1", 1, (255,255,255))
        scoretextother = myfont20.render("Player2", 1, (255,255,255))
        
        self.screen.blit(scoretextme, (10, 425))
        self.screen.blit(scoreme, (10, 435))
        self.screen.blit(scoretextother, (280, 425))
        self.screen.blit(scoreother, (340, 435))
    def finished(self):
        self.screen.blit(self.winningscreen, (0,0))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()   
          

    def next_possible_moves(self,move):
        #make the move true if the last move is not true to be true in the psuedo list
        if(move[2]==1):
            self.boardh_temp[move[0]][move[1]]=True;
        elif(move[2]==0):
            self.boardv_temp[move[0]][move[1]]=True;
        else: 
            print ("Invalid move");
        next_moves=[];
        
        for x in range (7):
            for y in range(6):
                if(self.boardh_temp[x][y]==False):
                    next_moves.append([x,y,1]); # append all horizontal moves
                
        for x in range (6):
            for y in range(7):
                if(self.boardv_temp[x][y]==False):
                    next_moves.append([x,y,0]); # append all horizontal moves
        
                
        return next_moves 
    def list_possible_moves(self,state_h,state_v):
        #make the move true if the last move is not true to be true in the psuedo list
        
        next_moves=[];
        for x in range (7):
            for y in range(6):
                if(state_h[x][y]==False):
                    next_moves.append([x,y,1]); # append all horizontal moves
                
                
                
        for x in range (6):
            for y in range(7):
                if(state_v[x][y]==False):
                    next_moves.append([x,y,0]); # append all horizontal moves
                
        
                
        return next_moves
    def current_state(self):
        return self.boardh,self.boardv
    
    def increment_score(self,move,h_matrix,v_matrix):
        temp_score=0;
        xpos=move[0];
        ypos=move[1];
        if(move[2]==0): # vertical matrices
            if(ypos==0):# left most edge
                if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
                    temp_score=1;
            elif(ypos==6):# left most edge   
                if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
                    temp_score=1;     
            else:
                if(h_matrix[xpos][ypos]==True and h_matrix[xpos+1][ypos]==True and v_matrix[xpos][ypos+1]==True):
                    temp_score=temp_score+1;
                if(h_matrix[xpos][ypos-1]==True and h_matrix[xpos+1][ypos-1]==True and v_matrix[xpos][ypos-1]==True):
                    temp_score=temp_score+1;
                    
        if(move[2]==1): # horizontal matrices
            if(xpos==0):
                if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
                    temp_score=1;
            elif(xpos==6):
                if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
                    temp_score=1;
                
            else:
                if(v_matrix[xpos][ypos]==True and v_matrix[xpos][ypos+1]==True and h_matrix[xpos+1][ypos]==True):
                    temp_score=temp_score+1;
                if(v_matrix[xpos-1][ypos]==True and v_matrix[xpos-1][ypos+1]==True and h_matrix[xpos-1][ypos]==True):
                    temp_score=temp_score+1;
                
                
            
        return temp_score;
    def make_move(self,move,player_id):
        print ('value before coming',self.boardh)
        xpos=move[0];
        ypos=move[1];
        #print xpos,ypos
        if(move[2]==1):# Vertical Matrices
            
            self.boardh[xpos][ypos]=True;
            
        if(move[2]==0):
            self.boardv[xpos][ypos]=True;
        self.boardh_temp = self.boardh
        self.boardv_temp = self.boardv
        #score=self.increment_score(move,self.boardh,self.boardv);
        #print self.boardh,self.boardv
        ### Leave space here for player color change 
        
        
        if(player_id==0):
            self.score_player1=self.score_player1+self.increment_score(move,self.boardh,self.boardv);
            if(move[2]==1):
                self.hColor[xpos][ypos]=-1;
            if(move[2]==0):
                print (xpos,ypos)
                self.vColor[xpos][ypos]=-1;
            
        if(player_id==1):
            self.score_player2=self.score_player2+self.increment_score(move,self.boardh,self.boardv);
            if(move[2]==1):
                self.hColor[xpos][ypos]=1;
            if(move[2]==0):
                self.vColor[xpos][ypos]=1;
    def next_state(self,move,h1,v1):
        xpos=move[0];
        ypos=move[1];
        h_matrix1=deepcopy(list(h1))
        v_matrix1=deepcopy(list(v1))
        
        
        score=self.increment_score(move,h_matrix1,v_matrix1);
        #print move[2];
        if(move[2]==0):#vetical matrices
            
            v_matrix1[xpos][ypos]=True;
            
            #self.boardv[xpos][ypos]=False
        if(move[2]==1):#horizontal matrices
            
            h_matrix1[xpos][ypos]=True;
            
            #self.boardh[xpos][ypos]=False
        #print move ,h_matrix,v_matrix
        return h_matrix1,v_matrix1,score;
    def game_ends(self,temp_h,temp_v):
        count=True;
        for x in range(6):
            for y in range(7):
                if not temp_h[y][x]:
                    count=False;
        for x in range(7):
            for y in range(6):
                if not temp_v[y][x]:
                    count=False;
        return count;
    
    def player1(self):
        temp_h=self.boardh
        temp_v=self.boardv
        
        next_move=self.list_possible_moves(temp_h,temp_v);
        
        best_move=next_move[0];
        best_score=0;
        
        for move in next_move:
            
            temp_h,temp_v,score=self.next_state(move,temp_h,temp_v);
            
            if(score>best_score):
                best_score=score;
                best_move=move;
        
        
        self.make_move(best_move,0);
        
    '''
    You will make changes to the code from this part onwards
    '''
    def player2(self):
        temp_h = self.boardh
        temp_v = self.boardv
        '''
        Call the minimax/alpha-beta pruning  function to return the optimal move
        '''
        
        ## change the next line of minimax/ aplpha-beta pruning according to your input and output requirments
        m = self.list_possible_moves(self.boardh, self.boardv)[0]     
        
        # Without Pruning
        # next_move = self.minimax(m, self.boardh, self.boardv, 2, True)
        # self.make_move(next_move, 1)
        # print('move_made by player 2', next_move)

        # With Pruning
        next_move_alpha = self.alphabetapruning(m, self.boardh, self.boardv, 1, True, float('-inf'), float('inf'))
        self.make_move(next_move_alpha, 1)
        print('move_made by player 2', next_move_alpha)
        
    '''
    Write down the code for minimax to a certain depth do no implement minimax all the way to the final state. 
    '''

     # You will implement the minimax algorithm in this function. You can change the 
     # number of input parameters of the function and the output of the function must 
     # be the optimal move made by the function.

    def minimax(self, next_move, horizontal, vertical, depth, max_player):
        start_time = time.time()
        moves = self.list_possible_moves(horizontal, vertical)
        if len(moves) <= 0 or depth <= 0:
            return next_move
        if max_player == True:
            max_eval = moves[0]
            for move in moves:
                next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
                new_eval = self.minimax(move, next_h, next_v, depth - 1, False)
                if self.evaluate(new_eval, next_h, next_v, max_player) > self.evaluate(max_eval, next_h, next_v, max_player):
                    max_eval = new_eval
            print("--- %s seconds ---" % (time.time() - start_time))
            return max_eval
        else:
            min_eval = moves[0]
            for move in moves:
                next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
                new_eval = self.minimax(move, next_h, next_v, depth - 1, True)
                if self.evaluate(new_eval, next_h, next_v, max_player) < self.evaluate(min_eval, next_h, next_v, max_player):
                    min_eval = new_eval
            print("--- %s seconds ---" % (time.time() - start_time))
            return min_eval


    def alphabetapruning(self, next_move, horizontal, vertical, depth, max_player, alpha, beta):
        start_time = time.time()
        moves = self.list_possible_moves(horizontal, vertical)
        if len(moves) <= 0 or depth <= 0:
            return next_move
        if max_player == True:
            max_eval = moves[0]
            for move in moves:
                next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
                new_eval = self.alphabetapruning(move, next_h, next_v, depth - 1, False, alpha, beta)
                eval_result = self.evaluate(new_eval, next_h, next_v, max_player)
                if eval_result > self.evaluate(max_eval, next_h, next_v, max_player):
                    max_eval = new_eval
                alpha = max(self.evaluate(max_eval, next_h, next_v, max_player), alpha)
                if beta <= alpha:
                    break
            print("--- %s seconds ---" % (time.time() - start_time))
            return max_eval
        else:
            min_eval = moves[0]
            for move in moves:
                next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
                new_eval = self.alphabetapruning(move, next_h, next_v, depth - 1, True, alpha, beta)
                eval_result = self.evaluate(new_eval, next_h, next_v, max_player)
                if eval_result < self.evaluate(min_eval, next_h, next_v, max_player):
                    min_eval = new_eval
                beta = min(self.evaluate(min_eval, next_h, next_v, max_player), beta)
                if beta <= alpha:
                    break
            print("--- %s seconds ---" % (time.time() - start_time))
            return min_eval

       
    '''
    Write down you own evaluation strategy in the evaluation function 
    '''
    def evaluate(self, move, horizontal, vertical, max_player):
        multiplier = 1
        if max_player == False:
            multiplier = -1
        next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
        eval_result = self.increment_score(move, horizontal, vertical)
        all_future_moves = self.list_possible_moves(next_h, next_v)
        max_score = 0
        for future_move in all_future_moves:
            score = self.increment_score(future_move, next_h, next_v)
            if score > max_score:
                max_score = score
        if eval_result > 0:
            return (eval_result * 2 - max_score) * multiplier
        else:
            return (-max_score) * multiplier
        

 
bg=BoxesandGridsGame();
while (bg.game_ends(bg.boardh,bg.boardv)==False):
    bg.update();
    print ('Player1 :score',bg.score_player1)
    print ('Player2 :score',bg.score_player2)
    time.sleep(2)
time.sleep(10)
pygame.quit()

# BACKUP
# def minimax(self,horizontal,vertical):
#         all_moves = self.list_possible_moves(horizontal, vertical)
#         max_score = -999
#         max_move = all_moves[0]
#         for move in all_moves:
#             score = self.evaluate(move, horizontal, vertical)
#             if score > max_score:
#                 max_score = score
#                 max_move = move
#         return max_move


#     def alphabetapruning(self,horizontal,vertical):
#         return 

       
#     '''
#     Write down you own evaluation strategy in the evaluation function 
#     '''
#     def evaluate(self, move, horizontal, vertical):
#         # Prioritize making own score move, then prevent enemy from scoring
#         next_h, next_v, f_s = self.next_state(move, horizontal, vertical)
#         eval_result = self.increment_score(move, horizontal, vertical)
#         all_future_moves = self.list_possible_moves(next_h, next_v)
#         max_score = 0
#         for future_move in all_future_moves:
#             score = self.increment_score(future_move, next_h, next_v)
#             if score > max_score:
#                 max_score = score
#         if eval_result > 0:
#             return eval_result * 2 + max_score
#         else:
#             return -max_score