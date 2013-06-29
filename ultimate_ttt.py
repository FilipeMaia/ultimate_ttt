#!/usr/bin/env python

import numpy as np
import random
import re
import copy


    
    

def init():
    state = {}
    state['board'] = np.zeros([9,9])
    state['to_move'] = 1
    state['finished'] = np.zeros([9,9])
    state['focus'] = np.ones([9,9])
    state['last_move'] = 1
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

def valid_move(state,move,verbose=True):
    if(not re.match('[a-i][1-9]',move)):
        if(verbose):
            print "Could not parse %s as a valid move" % (move)
        return False
    row,column = pos_to_row_col(move)
    if(state['board'][row,column] != 0):
        if(verbose):
            print "Square %s already occupied" % (move)
        return False
    focus = state['focus']
    if(not focus[row,column]):
        if(verbose):
            print "You must play on the currently active board!"
        return False
    return True


def pos_to_row_col(pos):
    column = ord(pos[0])-ord('a')
    row = int(pos[1])-1    
    return row,column

def row_col_to_pos(row,col):
    return chr(ord('a')+col)+str(row+1)

def winner(state):
    mini_board = state['finished'][::3,::3]
    return miniboard_winner(mini_board)

def board_winner(state,pos):
    row,col = pos_to_row_col(pos)
    row = 3*(row/3)
    col = 3*(col/3)
    mini_board = state['board'][row:row+3,col:col+3]
    return miniboard_winner(mini_board)

def miniboard_winner(mini_board):
    # Check rows
    for r in range(0,3):
        if(mini_board[r,0] == 0):
            continue
        if(np.all(mini_board[r,:] == mini_board[r,0])):
            return mini_board[r,0]
    # Check columns
    for c in range(0,3):
        if(mini_board[0,c] == 0):
            continue
        if(np.all(mini_board[:,c] == mini_board[0,c])):
            return mini_board[0,c]

    # Check diagonals
    if(mini_board[1,1] == 0):
        return 0
    if(mini_board[0,0] == mini_board[1,1] == mini_board[2,2]):
        return mini_board[1,1]
    if(mini_board[2,0] == mini_board[1,1] == mini_board[0,2]):
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
    score,move_chain = negamax(state,7,float('-inf'),float('inf'),1)
    print "%s: %s" %(move_chain,score)
    return move_chain[0]

def draw_board(state):
    line = '  '
    for c in range(0,9):
        if(c and c % 3 == 0):
            line += '| '
        line += chr(ord('a')+c)
        line += ' '
    print line

    for r in range(0,9):

        if(r and r %3 == 0):
            print '------------------------'
        line = '%d ' % (r+1)
        for c in range(0,9):
            if(c and c % 3 == 0):
                line += '| '
            if(state['board'][r,c] == 1):
                if(state['last_move'] and state['last_move'][0] == r and state['last_move'][1] == c):
                    line += '\033[1m' + 'x' + '\033[0m'
                else:
                    line += 'x'
            if(state['board'][r,c] == 2):
                if(state['last_move'] and state['last_move'][0] == r and state['last_move'][1] == c):
                    line += '\033[1m' + 'o' + '\033[0m'
                else:
                    line += 'o'
            if(state['board'][r,c] == 0):
                if(state['focus'][r,c]):
                    line += '#'
                else:
                    line += ' '
            line += ' '
        line += '%d ' % (r+1)
        print line
    line = '  '
    for c in range(0,9):
        if(c and c % 3 == 0):
            line += '| '
        line += chr(ord('a')+c)
        line += ' '
    print line
        

def play(state):
    while(winner(state) == 0):
        draw_board(state)
        print "Your score: %d" % (-score(state))
        print ''
        if(state['to_move'] != state['computer']):
            valid = False
            while(not valid):
                move = raw_input('Your move: ')
                valid = valid_move(state,move)
            make_move(state,move)            
        else:
            move = find_move(state)
            print 'My move: %s' % (move)
            make_move(state,move)
    draw_board(state)
    print ''        
    if(winner(state) == state['computer']):
        print "I won the game!"
    elif(winner(state)):
        print "You won the game!"
        
state = init()
play(state)
