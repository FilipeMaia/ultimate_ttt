#!/usr/bin/env python

import numpy as np
import random
import re
import copy
import sys
from gui import *
from engine import *
    
    


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
        
state = init(5)
if(len(sys.argv) > 1 and sys.argv[1] == '--gui'):
    init_gui(sys.argv)
else:
    play(state)
