# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:20:01 2017

@author: 317005
"""

from sym_struct import *
from sym_functions import *
from sym_evaluate import *
from sym_simplify import *
from sym_expand import *

def __main__():
    #print('teste')
    a = Node(NODE.OP, OP.MUL, [createInteger(5), createSymbol("a")])
    #print(toTree(a))
    b = Node(NODE.OP, OP.POW, [a, createSymbol("x")])
    c = Node(NODE.OP, OP.MUL, [a, a, b])
    #print(toTree(c))
    d = automatic_simplify(c)
    print(toTree(d))

if __name__ == "__main__":
    __main__()