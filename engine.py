import numpy as np
import random
import re
import copy

def init(depth,computer=0,humans=1):
    state = {}
    state['depth'] = depth
    state['board'] = np.zeros([9,9])
    state['to_move'] = 1
    state['finished'] = np.zeros([9,9])
    state['focus'] = np.ones([9,9])
    state['last_move'] = 0
    state['humans'] = humans
    if(humans == 2):
        state['computer'] = -1
    else:
        if(computer):
            state['computer'] = computer
        else:
            state['computer'] = random.randint(1,2)
        state['human'] = (state['computer']%2)+1
    return state


def make_move(state,move):
    row,col = pos_to_row_col(move)
    state['board'][row,col] = state['to_move']
    state['to_move'] = (state['to_move'] % 2) + 1
    if(board_winner(state,move) != 0):
        mark_as_won(state,move)

    # This must be done after checking for winners
    if(state['finished'][3*(row%3),3*(col%3)] != 0):
        state['focus'][:,:] = 1
    else:
        state['focus'][:,:] = 0
        state['focus'][3*(row%3):3*(row%3)+3,3*(col%3):3*(col%3)+3] = 1
    state['last_move'] = (row,col)

def valid_move(state,move,verbose=True,returnMessage=False):    
    if(not re.match('[a-i][1-9]',move)):
        msg = "Could not parse %s as a valid move" % (move)
        if(verbose):
            print msg
        if(returnMessage):
            return False,msg
        else:
            return False
    row,column = pos_to_row_col(move)
    if(state['board'][row,column] != 0):
        msg = "Square %s already occupied" % (move)
        if(verbose):
            print msg
        if(returnMessage):
            return False,msg
        else:
            return False
    focus = state['focus']
    if(not focus[row,column]):
        msg = "You must play on the currently active board"
        if(verbose):
            print msg
        if(returnMessage):
            return False,msg
        else:
            return False
    return True,""


def pos_to_row_col(pos):
    column = ord(pos[0])-ord('a')
    row = int(pos[1])-1    
    return row,column

def row_col_to_pos(row,col):
    return chr(ord('a')+col)+str(row+1)

def winner(state,line=False):
    mini_board = state['finished'][::3,::3]
    return miniboard_winner(mini_board,line)

def board_winner(state,pos):
    row,col = pos_to_row_col(pos)
    row = 3*(row/3)
    col = 3*(col/3)
    mini_board = state['board'][row:row+3,col:col+3]
    return miniboard_winner(mini_board)

def miniboard_winner(mini_board,line=False):
    # Check rows
    for r in range(0,3):
        if(mini_board[r,0] == 0):
            continue
        if(np.all(mini_board[r,:] == mini_board[r,0])):
            if(line):
                return mini_board[r,0],np.array([[r,0],[r,1],[r,2]])
            else:
                return mini_board[r,0]
    # Check columns
    for c in range(0,3):
        if(mini_board[0,c] == 0):
            continue
        if(np.all(mini_board[:,c] == mini_board[0,c])):
            if(line):
                return mini_board[0,c],np.array([[0,c],[1,c],[2,c]])
            else:
                return mini_board[0,c]

    # Check diagonals
    if(mini_board[1,1] == 0):
        return 0
    if(mini_board[0,0] == mini_board[1,1] == mini_board[2,2]):
        if(line):
            return mini_board[1,1],np.array([[0,0],[1,1],[2,2]])
        else:
            return mini_board[1,1]
    if(mini_board[2,0] == mini_board[1,1] == mini_board[0,2]):
        if(line):
            return mini_board[1,1],np.array([[2,0],[1,1],[0,2]])
        else:
            return mini_board[1,1]
    return 0

def mark_as_won(state,pos):
    player = board_winner(state,pos)
    row,col = pos_to_row_col(pos)
    row = 3*(row/3)
    col = 3*(col/3)
    for r in range(row,row+3):
        for c in range(col,col+3):
            state['board'][r,c] = player
            state['finished'][r,c] = player

def negamax(state,depth,alpha,beta,color):
    if(np.sum(state['board'] == 0) == 0):
        # It's a draw
        return 0,[]
    if(depth <= 0 or winner(state)):
        val = color*score(state)
        return val,[]
    moves = gen_moves(state)
    move_chain = []
    for m in range(0,len(moves[0])):
        move = row_col_to_pos(moves[0][m],moves[1][m])
        child_state = copy.deepcopy(state)
        make_move(child_state,move)
        child_alpha,child_move_chain = negamax(child_state,depth-1,-beta,-alpha,-color)
        if(-child_alpha >= beta):
            return -child_alpha,[move]+child_move_chain
        if(-child_alpha > alpha): 
            alpha = -child_alpha
            move_chain = [move]+child_move_chain
    return alpha,move_chain 
        
    
def score_line(line,state):
    if(state['computer'] == 1):
        sign = 1
    elif(state['computer'] == 2):
        sign = -1
    s = np.sum(line)
    if(s == 2):
        # This means we have two 1 and one 0
        return sign*1
    if(s == 4):
        # This means we have two 2 and one 0
        return -sign*1
    return 0

def score_miniboard(mini_board,state):
    if(np.all(mini_board == state['computer'])):
        return 100
    if(np.all(mini_board == state['human'])):
        return -100
    score = 0
    # Check rows
    for r in range(0,3):
        score += score_line(mini_board[r,:],state)
    # Check columns
    for c in range(0,3):
        score += score_line(mini_board[:,c],state)

    # Check diagonals
    if(mini_board[1,1] == 0):
        return 0
    if(mini_board[0,0] == mini_board[1,1] == mini_board[2,2]):
        return mini_board[1,1]
    if(mini_board[2,0] == mini_board[1,1] == mini_board[0,2]):
        return mini_board[1,1]


def score(state):
    score = 0
    w = winner(state)
    if(w == state['computer']):
        score += 10000
    elif(w == state['human']):
        score -= 10000
    score += np.sum(state['finished'] == state['computer'])*10
    score -= np.sum(state['finished'] == state['human'])*10
    
    return score

def gen_moves(state):
    return np.where(np.logical_and(state['board'] == 0,state['focus'] == 1))

def find_move(state):
    score,move_chain = negamax(state,state['depth'],float('-inf'),float('inf'),1)
#    print "%s: %s" %(move_chain,score)
    return move_chain[0]
