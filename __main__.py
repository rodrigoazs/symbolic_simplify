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
    print('teste')
    a = Node(NODE.OP, OP.ADD, [createInteger(1), createInteger(1),createInteger(1),createInteger(1),createInteger(1),createInteger(1)])
    b = automatic_simplify(a)
    print(b.children)

if __name__ == "__main__":
    __main__()